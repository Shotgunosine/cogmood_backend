#emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
#ex: set sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
# This file is part of the smile library. This following copyright notice
# applies to this file.
#
# smile - State Machine Interface Library for Experiments
#
# Copyright (C) 2012-2017
# Per B. Sederberg <psederberg@gmail.com>
#
# Authors: Per B. Sederberg
# URL: https://github.com/compmem/smile
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. It can be found in the file license.txt which
# is part of the smile package and online at
# <http://www.gnu.org/licenses/>.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

import gzip
import csv
import os

try:
    import cPickle as pickle
except ImportError:
    import pickle

class LogWriter(object):
    """An object that handles the writing of .slog files.

    *LogWriter* is what we use to write data to a .slog file. The
    *Log* state relies heavily on this object.

    Parameters
    ----------
    filename : string
        The filename that you would like to write to. Must end in .slog.
    protocol : int
        The pickle protocol to use. Defaults to 3.

    """

    def __init__(self, filename, protocol=3):
        self._file = gzip.open(filename, "wb")
        self._pickler = pickle.Pickler(self._file, protocol=protocol)
        self._pickler.fast = True

    def write_record(self, data):
        """Call this funciton to write a single row to the .slog file.

        Parameters
        ----------
        data : dict
            This is a dictionary where the keys are the
            field names that you are writing out to the .slog file.
        """
        # data must be a dict
        if not isinstance(data, dict):
            raise ValueError("data to log must be a dict instance.")
        self._pickler.dump(data)
        self._pickler.memo.clear()

    def close(self):
        self._file.close()


class LogReader(object):
    """An object that handles reading from .slog files.

    Passing in a filename, by calling **ReadRecord** you can read one
    row from the .slog file.

    Parameters
    ----------
    filename : string
        The name of the .slog that you wish to read.
    unwrap : boolean
        Whether to unwrap sub-dicts and tuples when reading.
    append_columns : dict
        Additional columns to add to each record.
    """
    def __init__(self, filename, unwrap=False, **append_columns):
        # set the file
        self._file = gzip.open(filename, "rb")

        # save whether we should unwrap when reading
        self._unwrap = unwrap

        # save additional columns to append
        self._append_columns = append_columns

        # set up the unpickler
        self._unpickler = pickle.Unpickler(self._file)

    def read_record(self):
        """Returns a dicitionary with the field names as keys.
        """
        try:
            # get the dict
            rec = self._unpickler.load()

            # unwrap it
            if self._unwrap:
                rec = _unwrap(rec)

            # append additional cols
            rec.update(self._append_columns)

            # return it
            return rec
        except (EOFError, IOError):
            return None

    def close(self):
        self._file.close()

    def __iter__(self):
        record = self.read_record()
        while record is not None:
            yield record
            record = self.read_record()
        self.close()


def _unwrap(d, prefix=''):
    """Process the items of a dict and unwrap them to the top level based
    on the key names.

    """
    new_item = {}
    for k in d:
        # add prefix
        key = prefix+k

        # see if dict
        if isinstance(d[k], dict):
            new_item.update(_unwrap(d[k], prefix=key+'_'))
            continue

        # see if tuple/list
        if isinstance(d[k], (tuple, list)):
            # turn into indexed dict
            tdict = {}
            for j in range(len(d[k])):
                tdict[str(j)] = d[k][j]
            new_item.update(_unwrap(tdict, prefix=key+'_'))
            continue

        # just add it in
        new_item[key] = d[k]

    return new_item


def _root_to_files(log_filename):
    """Get set of slogs from root."""
    if os.path.exists(log_filename):
        # there is just one
        log_files = [log_filename]
    else:
        # try appending numbers
        log_files = []
        for distinguisher in range(256):
            filename = "%s_%d.slog" % (log_filename,
                                       distinguisher)
            if os.path.exists(filename):
                log_files.append(filename)
            else:
                break
    return log_files


def log2dl(log_filename, unwrap=True, **append_columns):
    """Convert slog files to list of dicts (a dict-list).

    Parameters
    ----------
    log_filename : string
        Either a full filename with the slog extension or base
        name with everything up to the numerical index of a log,
        such as 'log_study', which will use the same algorithm
        that saved the files each time the experiment was run in
        in order to loop and read them all in.
    unwrap : boolean
        Whether to unwrap logged lists and dictionaries into a
        single row. e.g., 'log': {'time':10, 'error':.001} would
        turn into two columns: 'log_time' and 'log_error'.
    append_columns : kwargs
        Columns to add the same value to each row. Useful for adding
        a subject id to the data.

    Examples
    --------
    This method is particularly useful for loading data for analysis
    with Pandas. This example will load all logs that begin with
    "log_study" into a Pandas DataFrame, adding in a column for
    subject:

    ..
        import pandas as pd
        df = pd.DataFrame(log2dl('log_study', subject='exp001'))

    """
    # determine set of slogs
    log_files = _root_to_files(log_filename)
    if len(log_files) == 0:
        raise IOError("No matching slog files found.")

    # loop over slogs pulling out dicts
    dl = []
    for i, slog in enumerate(log_files):
        append_columns.update({'log_num': i})
        dl.extend([r for r in
                   LogReader(slog,
                             unwrap=unwrap,
                             **append_columns)])
    return dl


def log2csv(log_filename, csv_filename=None, **append_columns):
    """Convert slog files to a CSV.

    Parameters
    ----------
    log_filename : string
        Either a full filename with the slog extension or base
        name with everything up to the numerical index of a log,
        such as 'log_study', which will use the same algorithm
        that saved the files each time the experiment was run in
        in order to loop and read them all in.
    csv_filename : string
        Name of CSV file to write out. If None will use the
        log_filename
    append_columns : kwargs
        Columns to add the same value to each row. Useful for adding
        a subject id to the data.

    Examples
    --------
    This method is particularly useful for loading data for analysis
    with general stats programs, such as R. This example will convert
    all logs that begin with "log_study" into a CSV file "log_study.csv',
    adding a column for subject:

    ..
        log2csv('log_study', subject='exp001')

"""
    # determine set of slogs
    log_files = _root_to_files(log_filename)
    if len(log_files) == 0:
        raise IOError("No matching slog files found.")

    # get the set of colnames
    colnames = []
    for i, slog in enumerate(log_files):
        # update the append_columns
        append_columns.update({'log_num': i})
        for record in LogReader(slog, unwrap=True, **append_columns):
            for fieldname in record:
                if fieldname not in colnames:
                    colnames.append(fieldname)

    if csv_filename is None:
        # try making one out of the log_filename root
        csv_filename = os.path.splitext(log_filename)[0] + '.csv'

    # loop again and write out to file
    with open(csv_filename, 'wb') as fout:
        # open CSV and write header
        dw = csv.DictWriter(fout, fieldnames=list(colnames))
        dw.writeheader()

        # loop over log entries
        for i, slog in enumerate(log_files):
            # update the append_columns
            append_columns.update({'log_num': i})

            # loop over all records
            for record in LogReader(slog, unwrap=True, **append_columns):
                # handle unicode
                record = dict((k, v.encode('utf-8')
                               if isinstance(v, unicode)
                               else v)
                              for k, v in record.items())

                # write it out
                dw.writerow(record)
