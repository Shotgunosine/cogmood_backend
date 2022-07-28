---
layout: default
title: Using MTurk
nav_order: 5
parent: Basic usage
has_children: false
---

# Using MTurk
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

This page is a step-by-step guide to setting up an experiment on MTurk using Cloudresearch and NivTurk. It assumes that you already have working experiment code that has been tested both locally and on the server.

## Initialising the CloudResearch study
From the Dashboard, under 'Create a Study', click 'Mturk Toolkit'. This will create a new study. You should follow the steps there to fill in information about your study.

Below are the sections that have contents related to NivTurk.

### Setup HIT and Payment
- Set 'Survey Hyperlink' to `http://<ip-address>:<port-number>/`, as discussed on the [Serving experiments page](../serving). Make sure you include the forward slash `/` at the end, and make sure that you do not include the angle brackets.
- NivTurk expects several arguments to be provided from CloudResearch in the study URL (`workerId`, `assignmentId` and `hitId`). Make sure to keep the box for 'Do not add query string parameters' unselected (as default).

### How Workers are Approved
- NivTurk is configured for use with the Fixed Completion Code option.
- Cloudresearch will then provide a completion code. Copy this code and paste it into `app.ini` in the NivTurk folder (for details, see [here](../serving#set-completion-codes-prolific-only)).

## Useful information about CloudResearch studies

### MicroBatch and HyperBatch

MTurk charges fees for HITs: 20% if less than or equal to 9 participants per HIT, 40% if more than 9 participants. To avoid the over charge, CloudResearch offers the option of using MicroBatches: it batches the study into small HITs of 9 workers; when one HIT finishes, the next one will be launched automatically. Using MicroBatches, however, will lead to inevitable delay of launching the experiment. A better option is to use HyperBatch. This is a Pro Feature of CloudResearch, and is recommended.

### Preview the experiment before launching

Once you finish setting up the study, you will see it on Dashboard. You can click on the study, and then click 'CloudResearch Survey Preview'. This way, you can preview the experiment as participants see it.