const survey_json = {
      calculatedValues: [{
          name: "attn_fails",
          expression: "iif({baaars_inattention.attn__2} != 4 " +
              "and {baaars_inattention.attn__2} notempty, 1, 0) " +
              "+ iif({hitop_02.attn__3} != 2 " +
              "and {hitop_02.attn__3} notempty, 1, 0) " +
              "+ iif({hitop_08.attn__4} != 3 " +
              "and {hitop_08.attn__4} notempty, 1, 0) " +
              "+ iif({hitop_14.attn__5} != 0 " +
              "and {hitop_14.attn__5} notempty, 1, 0)",
          includeIntoResult: true
      }],
      triggers: [{
          "type": "complete",
          "expression": "{attn__1} = no"
      }, {
          "type": "complete",
          "expression": "{attn_fails} > 1"
      },
      ],
      pages: [{
          name: "demo",
          title: "Demographics",
          elements: [{
              type: "checkbox",
              name: "race",
              title: "Which most closely describes your racial group(s)?",
              choices: ["American Indian/Alaska Native", "Asian", "Native Hawaiian or Other Pacific Islander", "Black or African American", "White"],
              isRequired: true,
              showNoneItem: true,
              noneText: "Prefer not to answer",
          }, {
              type: "radiogroup",
              name: "ethnicity",
              title: "Which most closely describes your ethnic group?",
              choices: ['Not Hispanic or Latino', 'Hispanic or Latino'],
              isRequired: true,
              showNoneItem: true,
              noneText: "Prefer not to answer",
          }, {
              type: "radiogroup",
              name: "sex_at_birth",
              title: "What was your biological sex at birth?",
              choices: ['Female', 'Male', 'Prefer not to answer'],
              isRequired: true,
          }, {
              type: "text",
              name: "age",
              title: "How old are you (in years)?",
              maskType: "numeric",
              maskSettings: {
                  allowNegativeValues: false,
                  min: 0
              },
              isRequired: true,
          }
          ]
      }, {
          name: "ladder",
          title: "Demographics",
          elements: [{
              type: "html",
              name: "ladder",
              html: "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 788 1079' width='100%' >" +
    "<!-- Background image -->" +
    "<image href='../static/img/LadderImage_hiRes.png' x='0' y='0' />" +

    "<!-- Top rung -->" +
    "<polygon id='Top-rung' points='598,241 673,270 690,190 619,168' fill='transparent'>" +
        "<title>Top rung</title>" +
    "</polygon>" +

    "<!-- 2nd rung -->" +
    "<polygon id='2nd-rung' points='581,327 656,354 673,270 598,241' fill='transparent'>" +
        "<title>2nd rung</title>" +
    "</polygon>" +

    "<!-- 3rd rung -->" +
    "<polygon id='3rd-rung' points='563,411 638,439 656,354 581,327' fill='transparent'>" +
        "<title>3rd rung</title>" +
    "</polygon>" +

    "<!-- 4th rung -->" +
    "<polygon id='4th-rung' points='546,496 620,523 638,439 563,411' fill='transparent'>" +
        "<title>4th rung</title>" +
    "</polygon>" +

    "<!-- 5th rung -->" +
    "<polygon id='5th-rung' points='529,580 603,608 620,523 546,496' fill='transparent'>" +
        "<title>5th rung</title>" +
    "</polygon>" +

    "<!-- 6th rung -->" +
    "<polygon id='6th-rung' points='510,665 585,693 603,608 529,580' fill='transparent'>" +
        "<title>6th rung</title>" +
    "</polygon>" +

    "<!-- 7th rung -->" +
    "<polygon id='7th-rung' points='493,749 568,777 585,693 510,665' fill='transparent'>" +
        "<title>7th rung</title>" +
    "</polygon>" +

    "<!-- 8th rung -->" +
    "<polygon id='8th-rung' points='477,833 551,862 568,777 493,749' fill='transparent'>" +
        "<title>8th rung</title>" +
    "</polygon>" +

    "<!-- 9th rung -->" +
    "<polygon id='9th-rung' points='458,917 533,946 551,862 477,833' fill='transparent'>" +
        "<title>9th rung</title>" +
    "</polygon>" +

    "<!-- Bottom rung -->" +
    "<polygon id='Bottom-rung' points='440,1005 515,1033 533,946 458,917' fill='transparent'>" +
        "<title>Bottom rung</title>" +
    "</polygon>" +
"</svg>"
,
              startWithNewLine: false
          }, {
              type: "radiogroup",
              name: "ladder_resp",
              title: "Where would you place yourself on the ladder?",
              choices: ['Top rung', '2nd rung', '3rd rung', '4th rung', '5th rung', '6th rung', '7th rung', '8th rung', '9th rung', 'Bottom rung'],
              isRequired: true,
          }],
      }, {
          name: "screen",
          elements: [{
              type: "radiogroup",
              name: "ongoing_mentalhealth",
              title: "Do you have – or have you had – a diagnosed, on-going mental health/illness/condition?",
              choices: ['Yes', 'No',],
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "mentalhealth_daily_impact",
              title: "Do you have any diagnosed mental health condition that is uncontrolled (by medication or intervention) and which has a significant impact on your daily life / activities?",
              choices: ['Yes', 'No'],
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "experience_depression",
              title: "Do you experience depression?",
              choices: ['Yes', 'No'],
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "experience_anxiety",
              title: "Do you experience anxiety?",
              choices: ['Yes', 'No'],
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "have_adhd",
              title: "Do you consider yourself to have attention deficit disorder (ADD)/attention deficit hyperactivity disorder (ADHD)?",
              choices: ['Yes', 'No'],
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "attn__1",
              title: "Are you willing to download and run tasks on your computer? If not, the survey will complete after this page and you will be redirected to Prolific.",
              choices: ['Yes', 'No'],
              isRequired: true,
          }
          ]
      }, {
          name: "fried",
          elements: [{
              type: "comment",
              name: "fried",
              title: "In the box below, please indicate what you think is the most important cause for someone developing depression.",
              description: "There is no right or wrong answer, we would just like to know what you think.",
              rows: 2,
              autoGrow: true,
              isRequired: true,
          }
          ]
      }, {
          name: "diag_deets_1",
          title: "Mood disorder diagnosis",
          elements: [{
              type: "radiogroup",
              name: "mood_pro_diagnosis",
              title: "Have you been diagnosed with a mood disorder by a mental health professional? This includes: " +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Depression, " +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Major Depressive Disorder, " +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Bipolar Disorder type I or II, " +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cyclothymic Disorder," +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Persistent Depressive Disorder (Dysthymia), " +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Premenstrual Dysphoric Disorder.",
              choices: ['Yes', 'No', 'Prefer not to answer'],
              isRequired: true,
          },
          ]
      }, {
          name: "diag_deets_2",
          title: "Mood disorder details",
          visibleIf: "{mood_pro_diagnosis} = yes",
          elements: [{
              type: "checkbox",
              name: "mood_diagnoses",
              title: "Which mood disorders have you been diagnosed with? Please select all that apply.",
              choices: [
                  'Major Depressive Disorder',
                  'Persistent Depressive Disorder',
                  '(Dysthymia)Premenstrual Dysphoric Disorder',
                  'Bipolar I Disorder',
                  'Bipolar II Disorder',
                  'Cyclothymic Disorder'
              ],
              showOtherItem: true,
              otherText: "Other (please specify)",
              showNoneItem: true,
              noneText: "Prefer not to answer",
              isRequired: true,
          }, {
              type: "text",
              name: "mood_first_dx_years",
              title: "How many years ago were you first diagnosed with a mood disorder (to the best of your ability to recall)?",
              maskType: "numeric",
              maskSettings: {
                  allowNegativeValues: false,
                  max: 100,
                  min: 0
              },
              isRequired: true,
          }, {
              type: "checkbox",
              name: "mood_treatment",
              title: "Are you currently receiving treatment for this disorder, if so, which types? Please select all treatments that you have received in the last month that are intended to treat your mood disorder(s).",
              choices: [
                  "I am not receiving treatment for a mood disorder",
                  "One-on-one talk therapy with a professional",
                  "Group therapy",
                  "Selective Serotonin Reuptake Inhibitor (SSRI), such as: Prozac (fluoxotine), Celexa (citalopram), Lexapro (escitalopram), Paroxetine (Paxil), Sertraline (Zoloft)",
                  "Serotonin and Norepinephrine Reuptake Inhibitor (SNRI), such as: Cymbalta (duloxetine), Effexor (venalfaxine)",
                  "Tricyclic Antidepressant (TCA), such as: Anafranil (clomipramine), Sinequan (doxepin)",
                  "Monoamine Oxidase Inhibitor (MAOI), such as: Emsam (selegiline), Marplan (isocarboxaxid)",
                  "Serotonin Antagonist and Reuptake Inhibitors, such as: Oleptro (trazodone), Brintellix (vortioxetine)",
                  "Remeron (mirtazapine)",
                  "Symbax (olanzapine/fluoxotine)",
                  "Wellbutrin (buproprion)",
                  "Lithium",
                  "Depakane (valproate), Epival (divalproex)",
                  "Tegretol (carbamazepine), Trileptal (oxcarbazepine)",
                  "Lamictal (lamotrigine)",
                  "Haloperidol (haldol decanoate)",
                  "Abilify (aripiprazole), Saphris (asenapine), Vraylar (cariprazine), Zyprexa (olanzapine), Risperdal (risperdone)",
                  "Latuda (lurasidone)",
                  "Caplyta (lumaterperone), Seroquel (quetiapine)"
              ],
              showOtherItem: true,
              otherText: "Other (please specify)",
              showNoneItem: true,
              noneText: "Prefer not to answer",
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "mood_med_today",
              title: "Have you taken medication for your mood disorder today?",
              choices: ['Yes', 'No', 'Not applicable (Not taking medication for a mood disorder)'],
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "mood_bothered",
              title: "In the past two weeks have you been bothered by symptoms of your mood disorder(s)?",
              choices: ['Yes', 'No', 'Prefer not to answer'],
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "mood_bothered_today",
              title: "Have you been bothered by symptoms of your mood disorder(s) today?",
              choices: ['Yes', 'No', 'Prefer not to answer'],
              isRequired: true,
          }
          ]

      }, {
          name: "diag_deets_3",
          title: "Anxiety disorder diagnosis",
          elements: [{
              type: "radiogroup",
              name: "anxiety_pro_diagnosis",
              title: "Have you been diagnosed with an anxiety disorder by a mental health professional? This includes:" +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Generalized Anxiety Disorder," +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Separation Anxiety Disorder," +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Agoraphobia," +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Specific Phobia," +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Social Anxiety Disorder (Social Phobia)," +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Panic Disorder," +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Panic Attack," +
                  "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Selective Mutism",
              choices: ['Yes', 'No', 'Prefer not to answer'],
              isRequired: true,
          },
          ]
      }, {
          name: "diag_deets_4",
          title: "Anxiety disorder details",
          visibleIf: "{anxiety_pro_diagnosis} = yes",
          elements: [{
              type: "checkbox",
              name: "anxiety_diagnoses",
              title: "Which anxiety disorders have you been diagnosed with? Please select all that apply.",
              choices: [
                  'Generalized Anxiety Disorder',
                  'Separation Anxiety Disorder',
                  'Agoraphobia',
                  'Specific Phobia',
                  'Social Anxiety Disorder (Social Phobia)',
                  'Panic Disorder',
                  'Panic Attack',
                  'Selective Mutism'
              ],
              showOtherItem: true,
              otherText: "Other (please specify)",
              showNoneItem: true,
              noneText: "Prefer not to answer",
              isRequired: true,
          }, {
              type: "text",
              name: "anxiety_first_dx_years",
              title: "How many years ago were you first diagnosed with an anxiety disorder (to the best of your ability to recall)?",
              maskType: "numeric",
              maskSettings: {
                  allowNegativeValues: false,
                  max: 100,
                  min: 0
              },
              isRequired: true,
          }, {
              type: "checkbox",
              name: "anxiety_treatment",
              title: "Are you currently receiving treatment for this disorder, if so, which types? Please select all treatments that you have received in the last month that are intended to treat your anxiety disorder(s).",
              choices: [
                  "I am not receiving treatment for an anxiety disorder",
                  "One-on-one talk therapy with a professional",
                  "Group therapy",
                  "Selective Serotonin Reuptake Inhibitor (SSRI), such as: Prozac (fluozotine), Celexa (citalopram), Lexapro (escitalopram), Paroxetine (Paxil), Sertraline (Zoloft)",
                  "Serotonin and Norepinephrine Reuptake Inhibitor (SNRI), such as: Cymbalta (duloxetine), Effexor (venalfaxine)",
                  "Tricyclic Antidepressant (TCA), such as: Anafranil (clomipramine), Sinequan (doxepin)",
                  "Benzodiazepine, such as: Xanax (alprazolam), Valium (diazepam), Ativan (lorazepam), Librium (chlordiazepoxide)",
                  "Monoamine Oxidase Inhibitor (MAOI), such as: Emsam (selegiline), Marplan (isocarboxaxid)",
                  "Beta-blocker, such as: Tenormin (atenolol), Inderal (propranolol)",
                  "BuSpar (buspirone)",
              ],
              showOtherItem: true,
              otherText: "Other (please specify)",
              showNoneItem: true,
              noneText: "Prefer not to answer",
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "anxiety_med_today",
              title: "Have you taken medication for your anxiety disorder today?",
              choices: ['Yes', 'No', 'Not applicable (Not taking medication for an anxiety disorder)'],
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "anxiety_bothered",
              title: "In the past two weeks have you been bothered by symptoms of your anxiety disorder(s)?",
              choices: ['Yes', 'No', 'Prefer not to answer'],
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "anxiety_bothered_today",
              title: "Have you been bothered by symptoms of your anxiety disorder(s) today?",
              choices: ['Yes', 'No', 'Prefer not to answer'],
              isRequired: true,
          }
          ]

      }, {
          name: "diag_deets_5",
          title: "Attention disorder diagnosis",
          elements: [{
              type: "radiogroup",
              name: "attention_pro_diagnosis",
              title: "Have you been diagnosed with attention-deficit/hyperactivity disorder (ADHD) or attention-deficit disorder (ADD)?",
              choices: ['Yes', 'No', 'Prefer not to answer'],
              isRequired: true,
          },
          ]
      }, {
          name: "diag_deets_6",
          title: "Attention disorder details",
          visibleIf: "{attention_pro_diagnosis} = yes",
          elements: [{
              type: "checkbox",
              name: "attention_diagnoses",
              title: "Which attention disorders have you been diagnosed with? Please select all that apply.",
              choices: [
                  'Attention-Deficit/Hyperactivity Disorder (ADHD)',
                  'Attention-Deficit Disorder (ADD)',
              ],
              showOtherItem: true,
              otherText: "Other (please specify)",
              showNoneItem: true,
              noneText: "Prefer not to answer",
              isRequired: true,
          }, {
              type: "text",
              name: "attention_first_dx_years",
              title: "How many years ago were you first diagnosed with an attention disorder (to the best of your ability to recall)?",
              maskType: "numeric",
              maskSettings: {
                  allowNegativeValues: false,
                  max: 100,
                  min: 0
              },
              isRequired: true,
          }, {
              type: "checkbox",
              name: "attention_treatment",
              title: "Are you currently receiving treatment for this disorder, if so, which types? Please select all treatments that you have received in the last month that are intended to treat your anxiety disorder(s).",
              choices: [
                  "I am not receiving treatment for an attention disorder",
                  "One-on-one talk therapy with a professional",
                  "Group therapy",
                  "Amphetamine, such as Dexedrine (dextroamphetamine), Adderall (amphetamine salts), Vyvanse (lisdexamfetamine)",
                  "Methylphenidate, such as Concerta, Ritalin, Focalin (dexmethylphenidate)",
                  "Strattera (atomoxetine)",
                  "Wellbutrin (buproprion)",
                  "Intuniv (guanfacine)",
                  "Catapres, Kapvay (clonidine)",
              ],
              showOtherItem: true,
              otherText: "Other (please specify)",
              showNoneItem: true,
              noneText: "Prefer not to answer",
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "attention_med_today",
              title: "Have you taken medication for your attention disorder today?",
              choices: ['Yes', 'No', 'Not applicable (Not taking medication for an attention disorder)'],
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "attention_bothered",
              title: "In the past two weeks have you been bothered by symptoms of your attention disorder(s)?",
              choices: ['Yes', 'No', 'Prefer not to answer'],
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "attention_bothered_today",
              title: "Have you been bothered by symptoms of your attention disorder(s) today?",
              choices: ['Yes', 'No', 'Prefer not to answer'],
              isRequired: true,
          }
          ]

      }, {
          name: "stdqs_1",
          title: "Inattention",
          elements: [{
              alternateRows: true,
              type: "matrix",
              name: "baaars_inattention",
              title: "For each item, please select the option that describes your behavior during the ****last 2 weeks****.",
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              isAllRowRequired: true,
              columns: [{
                  value: 1,
                  text: "Never or rarely",
              }, {
                  value: 2,
                  text: "Sometimes",
              }, {
                  value: 3,
                  text: "Often",
              }, {
                  value: 4,
                  text: "Very Often",
              }],
              rows: [{
                  value: "baars_inattentive_1",
                  text: "Fail to give close attention to details or make careless mistakes in my work or other activities",
              }, {
                  value: "baars_inattentive_2",
                  text: "Difficulty sustaining my attention in tasks or fun activities",
              }, {
                  value: "baars_inattentive_3",
                  text: "Don't listen when spoken to directly",
              }, {
                  value: "baars_inattentive_4",
                  text: "Don't follow through on instructions and fail to finish work or chores",
              }, {
                  value: "baars_inattentive_5",
                  text: "Have difficulty organizing tasks and activities",
              }, {
                  value: "baars_inattentive_6",
                  text: "Avoid, dislike, or am reluctant to engage in tasks that require sustained mental effort",
              }, {
                  value: "attn__2",
                  text: 'To check if you are a true respondent, please select "Very often" for this item.',
              }, {
                  value: "baars_inattentive_7",
                  text: "Lose things necessary for tasks or activities",
              }, {
                  value: "baars_inattentive_8",
                  text: "Easily distracted by extraneous stimuli or irrelevant thoughts",
              }, {
                  value: "baars_inattentive_9",
                  text: "Forgetful in daily activities",
              }
              ]
          }
          ]

      }, {
          name: "stdqs_2",
          title: "Hyperactivity",
          elements: [{
              type: "matrix",
              name: "baaars_hyperactivity",
              title: "For each item, please select the option that describes your behavior during the **last 2 weeks**.",
              isAllRowRequired: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              alternateRows: true,
              columns: [{
                  value: 1,
                  text: "Never or rarely",
              }, {
                  value: 2,
                  text: "Sometimes",
              }, {
                  value: 3,
                  text: "Often",
              }, {
                  value: 4,
                  text: "Very Often",
              }],
              rows: [{
                  value: "baars_hyperactivity_1",
                  text: "Fidget with hands or feet or squirm in seat",
              }, {
                  value: "baars_hyperactivity_2",
                  text: "Leave my seat in classrooms or in other situations in which remaining seated is expected",
              }, {
                  value: "baars_hyperactivity_3",
                  text: "Shift around excessively or feel restless or hemmed in",
              }, {
                  value: "baars_hyperactivity_4",
                  text: "Have difficulty engaging in leisure activities quietly (feel uncomfortable, or am loud or noisy)",
              }, {
                  value: "baars_hyperactivity_5",
                  text: 'I am "on the go" or act as if "driven by a motor" (or I feel like I have to be busy or always doing something)',
              }]
          }]
      }, {
          name: "stdqs_3",
          title: "Impulsivity",
          elements: [{
              type: "matrix",
              name: "baaars_impulsivity",
              title: "For each item, please select the option that describes your behavior during the **last 2 weeks**.",
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              isAllRowRequired: true,
              alternateRows: true,
              columns: [{
                  value: 1,
                  text: "Never or rarely",
              }, {
                  value: 2,
                  text: "Sometimes",
              }, {
                  value: 3,
                  text: "Often",
              }, {
                  value: 4,
                  text: "Very Often",
              }],
              rows: [{
                  value: "baars_impulsivity_1",
                  text: "Talk excessively (in social situations)",
              }, {
                  value: "baars_impulsivity_2",
                  text: "Blurt out answers before questions have been completed, complete others' sentences, or jump the gun",
              }, {
                  value: "baars_impulsivity_3",
                  text: "Have difficulty awaiting my turn",
              }, {
                  value: "baars_impulsivity_4",
                  text: "Interrupt or intrude on others (butt into conversations or activities without permission or take over what others are doing)",
              }]
          }]
      }, {
          name: "stdqs_4",
          title: "Sluggish Cognitive Tempo",
          elements: [{
              type: "matrix",
              name: "baaars_sct",
              title: "For each item, please select the option that describes your behavior during the **last 2 weeks**.",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 1,
                  text: "Never or rarely",
              }, {
                  value: 2,
                  text: "Sometimes",
              }, {
                  value: 3,
                  text: "Often",
              }, {
                  value: 4,
                  text: "Very Often",
              }],
              rows: [{
                  value: "baars_sct_1",
                  text: "Prone to daydreaming when I should be concentrating on something or working",
              }, {
                  value: "baars_sct_2",
                  text: "Have trouble staying alert or awake in boring situations",
              }, {
                  value: "baars_sct_3",
                  text: "Easily confused",
              }, {
                  value: "baars_sct_4",
                  text: "Easily bored",
              }, {
                  value: "baars_sct_5",
                  text: 'Spacey or "in a fog"',
              }, {
                  value: "baars_sct_6",
                  text: "Lethargic, more tired than others",
              }, {
                  value: "baars_sct_7",
                  text: "Underactive or have less energy than others",
              }, {
                  value: "baars_sct_8",
                  text: "Slow moving",
              }, {
                  value: "baars_sct_9",
                  text: "I don't seem to process information as quickly or as accurately as others",
              }]
          }]
      }, {
          name: "stdqs_5",
          title: "GAD-7",
          elements: [{
              type: "matrix",
              name: "gad7_",
              title: "Over the **last two weeks**, how often have you been bothered by the following problems?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "Several days",
              }, {
                  value: 2,
                  text: "More than half the days",
              }, {
                  value: 3,
                  text: "Nearly every day",
              }],
              rows: [{
                  value: "gad7__1",
                  text: "Feeling nervous, anxious or on edge",
              }, {
                  value: "gad7__2",
                  text: "Not being able to stop or control worrying",
              }, {
                  value: "gad7__3",
                  text: "Worrying too much about different things",
              }, {
                  value: "gad7__4",
                  text: "Trouble relaxing",
              }, {
                  value: "gad7__5",
                  text: 'Being so restless that it is hard to sit still',
              }, {
                  value: "gad7__6",
                  text: "Becoming easily annoyed or irritable",
              }, {
                  value: "gad7__7",
                  text: "Feeling afraid, as if something awful might happen",
              }]
          }]
      }, {
          name: "stdqs_6",
          title: "PHQ-8",
          elements: [{
              type: "matrix",
              name: "phq8_",
              title: "Over the **last two weeks**, how often have you been bothered by the following problems?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "Several days",
              }, {
                  value: 2,
                  text: "More than half the days",
              }, {
                  value: 3,
                  text: "Nearly every day",
              }],
              rows: [{
                  value: "phq8__1",
                  text: "Little interest or pleasure in doing things",
              }, {
                  value: "phq8__2",
                  text: "Feeling down, depressed, irritable or hopeless",
              }, {
                  value: "phq8__3",
                  text: "Trouble falling or staying asleep, or sleeping too much",
              }, {
                  value: "phq8__4",
                  text: "Feeling tired or having little energy",
              }, {
                  value: "phq8__5",
                  text: 'Poor appetite or overeating',
              }, {
                  value: "phq8__6",
                  text: "Feeling bad about yourself – or that you are a failure or have let yourself or your family down",
              }, {
                  value: "phq8__7",
                  text: "Trouble concentrating on things, such as school work, reading or watching television",
              }, {
                  value: "phq8__8",
                  text: "Moving or speaking so slowly that other people could have noticed? Or the opposite – being so fidgety or restless that you have been moving around a lot more than usual",
              }]
          }]
      }, {
          name: "hitop_i1",
          title: "CogMood Surveys",
          showQuestionNumbers: false,
          elements: [{
              type: "html",
              name: "hitopintro1",
              html: 'In this survey, you will be asked to respond to a number of statements about your thoughts, feelings, and behavior. Some of these things are pretty common, whereas others are less common. As you complete the survey, please consider whether there have been significant times during the <strong> **last 2 weeks** </strong> during which the following statements applied to you. Then please select the option that best describes how well each statement described you during that period.',
              startWithNewLine: false
          }],
      }, {
          name: "hitop_i2",
          title: "CogMood Surveys",
          showQuestionNumbers: false,
          elements: [{
              type: "html",
              name: "hitopintro2",
              html: 'Some statements will ask you to select a specific response. For example, if you see the statement <strong> "I felt like selecting a little" </strong> please select "<strong>A Little</strong>". <p><p>These statements do blend in with the other statements, so <strong> please read each statement carefully </strong>. We include these checks to ensure that we are collecting high quality data from real humans who are paying attention to the questions. Poor data quality will make it harder to for us to learn about the relationships between how people think and symptoms of mental health disorders. If you miss too many of these check questions, you will only be compensated for completing the survey and will not be asked to complete the cognitive tasks.',
              startWithNewLine: false
          }],
      }, {
          name: "hitop_01",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_01",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_anhdep_1",
                  text: "I had very little energy.",
              }, {
                  value: "hitop_sepinsec_1",
                  text: "I worried that others would abandon me.",
              }, {
                  value: "hitop_anxwor_1",
                  text: "Thoughts were racing through my head.",
              }, {
                  value: "hitop_welbe_1",
                  text: "It was easy for me to laugh.",
              }, {
                  value: "hitop_appgn_1",
                  text: 'I stuffed myself with food.',
              }, {
                  value: "hitop_anhdep_2",
                  text: "I was unable to enjoy things like I normally do.",
              }]
          }]
      }, {
          name: "hitop_02",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_02",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_sepinsec_2",
                  text: "I wanted other people to take care of me.",
              }, {
                  value: "hitop_anxwor_2",
                  text: "I had a lot of nervous energy.",
              }, {
                  value: "hitop_sepinsec_3",
                  text: "I wanted someone else to make decisions for me.",
              }, {
                  value: "attn__3",
                  text: 'To check if you are a true respondent, please select "Moderately" for this item.',
              }, {
                  value: "hitop_socanx_1",
                  text: 'I avoided performing or giving a talk in front of others.',
              }, {
                  value: "hitop_anxwor_3",
                  text: "I was overwhelmed by anxiety.",
              }]
          }]
      }, {
          name: "hitop_03",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_03",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_socanx_2",
                  text: "I avoided situations in which others were likely to watch me.",
              }, {
                  value: "hitop_hypsom_1",
                  text: "I felt like I could go for days without sleeping.",
              }, {
                  value: "hitop_anhdep_3",
                  text: "Nothing seemed interesting to me.",
              }, {
                  value: "hitop_cogprb_1",
                  text: 'I could not stay focused on what I was doing.',
              }, {
                  value: "hitop_welbe_2",
                  text: 'I looked forward to things with enjoyment.',
              }, {
                  value: "hitop_welbe_3",
                  text: 'I felt that I had a lot to look forward to.',
              }]
          }]
      }, {
          name: "hitop_04",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_04",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_appgn_2",
                  text: "I thought a lot about food.",
              }, {
                  value: "hitop_sepinsec_4",
                  text: "I felt insecure about important relationships in my life.",
              }, {
                  value: "hitop_socanx_3",
                  text: "I felt uncomfortable being the center of attention.",
              }, {
                  value: "hitop_indec_1",
                  text: 'I was indecisive.',
              }, {
                  value: "hitop_socanx_4",
                  text: 'I felt self-conscious around others.',
              }, {
                  value: "hitop_appls_1",
                  text: 'My appetite was poor.',
              }]
          }]
      }, {
          name: "hitop_05",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_05",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_anhdep_4",
                  text: "I felt depressed.",
              }, {
                  value: "hitop_appgn_3",
                  text: "I could not keep myself from eating.",
              }, {
                  value: "hitop_anhdep_5",
                  text: "I didn’t look forward to seeing friends or family.",
              }, {
                  value: "hitop_anhdep_6",
                  text: 'It took a lot of effort to do everyday activities.',
              }, {
                  value: "hitop_socanx_5",
                  text: 'I found it difficult to speak up in front of others.',
              }, {
                  value: "hitop_anhdep_7",
                  text: 'It felt like there wasn’t anything interesting or fun to do.',
              }]
          }]
      }, {
          name: "hitop_06",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_06",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_insom_1",
                  text: "I slept very poorly.",
              }, {
                  value: "hitop_panic_1",
                  text: "My hands were cold or sweaty.",
              }, {
                  value: "hitop_indec_2",
                  text: "I had trouble making up my mind.",
              }, {
                  value: "hitop_welbe_4",
                  text: 'I was proud of myself.',
              }, {
                  value: "hitop_appls_2",
                  text: 'I lost a significant amount of weight without even trying.',
              }, {
                  value: "hitop_sitphb_1",
                  text: 'I avoided riding in elevators.',
              }]
          }]
      }, {
          name: "hitop_07",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_07",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_anxwor_4",
                  text: "I felt tense.",
              }, {
                  value: "hitop_cogprb_2",
                  text: "I was easily distracted.",
              }, {
                  value: "hitop_socanx_6",
                  text: "I felt shy around other people.",
              }, {
                  value: "hitop_sepinsec_5",
                  text: 'I often felt jealous.',
              }, {
                  value: "hitop_anhdep_8",
                  text: 'I was a lot less talkative than usual.',
              }, {
                  value: "hitop_anxwor_5",
                  text: 'I worried about almost everything.',
              }]
          }]
      }, {
          name: "hitop_08",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_08",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_panic_2",
                  text: "I felt dizzy or lightheaded.",
              }, {
                  value: "attn__4",
                  text: "I felt like selecting a lot.",
              }, {
                  value: "hitop_socanx_7",
                  text: "I had difficulty making eye contact with others.",
              }, {
                  value: "hitop_socanx_8",
                  text: 'I felt socially awkward.',
              }, {
                  value: "hitop_welbe_5",
                  text: 'I felt like I had a lot of interesting things to do.',
              }, {
                  value: "hitop_welbe_6",
                  text: 'I found compliments very encouraging.',
              }]
          }]
      }, {
          name: "hitop_09",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_09",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_insom_2",
                  text: "I had trouble staying asleep.",
              }, {
                  value: "hitop_welbe_7",
                  text: "I felt cheerful.",
              }, {
                  value: "hitop_sitphb_2",
                  text: "I was afraid of flying.",
              }, {
                  value: "hitop_welbe_8",
                  text: 'I felt optimistic.',
              }, {
                  value: "hitop_welbe_9",
                  text: 'I felt like I was having a lot of fun.',
              }, {
                  value: "hitop_cogprb_3",
                  text: 'I had trouble remembering things.',
              }]
          }]
      }, {
          name: "hitop_10",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_10",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_anhdep_9",
                  text: "I felt emotionally numb.",
              }, {
                  value: "hitop_welbe_10",
                  text: "I felt good about myself.",
              }, {
                  value: "hitop_sitphb_3",
                  text: "I was afraid of heights.",
              }, {
                  value: "hitop_hypsom_2",
                  text: 'I needed much less sleep than usual.',
              }, {
                  value: "hitop_hypsom_3",
                  text: 'I did not feel tired, even though I was sleeping less than usual.',
              }, {
                  value: "hitop_anxwor_6",
                  text: 'I felt nervous and "on edge."',
              }]
          }]
      }, {
          name: "hitop_11",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_11",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_socanx_9",
                  text: "I was uncomfortable entering a room when others already were present.",
              }, {
                  value: "hitop_indec_3",
                  text: "It was difficult for me to make decisions.",
              }, {
                  value: "hitop_sepinsec_6",
                  text: "I could not handle rejection.",
              }, {
                  value: "hitop_sitphb_4",
                  text: 'I became very anxious during a storm.',
              }, {
                  value: "hitop_anxwor_7",
                  text: 'I felt very stressed.',
              }, {
                  value: "hitop_cogprb_4",
                  text: 'I was unable to keep my mind on what I was doing.',
              }]
          }]
      }, {
          name: "hitop_12",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_12",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_anhdep_10",
                  text: "Nothing made me laugh.",
              }, {
                  value: "hitop_appgn_4",
                  text: "I ate even when I was not really hungry.",
              }, {
                  value: "hitop_insom_3",
                  text: "I lay awake for a long time before falling asleep.",
              }, {
                  value: "hitop_sitphb_5",
                  text: 'I was afraid of the dark.',
              }, {
                  value: "hitop_shmglt_1",
                  text: 'I felt guilty.',
              }, {
                  value: "hitop_sepinsec_7",
                  text: 'I felt that I needed the approval of others.',
              }]
          }]
      }, {
          name: "hitop_13",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_13",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_hypsom_4",
                  text: "I felt like I could keep going and going without ever getting tired.",
              }, {
                  value: "hitop_panic_3",
                  text: "I was trembling or shaking.",
              }, {
                  value: "hitop_socanx_10",
                  text: "I was uncomfortable meeting new people.",
              }, {
                  value: "hitop_panic_4",
                  text: 'My heart was racing or pounding.',
              }, {
                  value: "hitop_hypsom_5",
                  text: 'I had days when I never got tired.',
              }, {
                  value: "hitop_insom_4",
                  text: 'I woke up early and could not get back to sleep.',
              }]
          }]
      }, {
          name: "hitop_14",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_14",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_shmglt_2",
                  text: "I felt ashamed of things I had done.",
              }, {
                  value: "hitop_panic_5",
                  text: "I was short of breath.",
              }, {
                  value: "hitop_shmglt_3",
                  text: 'I was disgusted with myself.',
              }, {
                  value: "hitop_shmglt_4",
                  text: 'I blamed myself for things.',
              }, {
                  value: "attn__5",
                  text: "I was selecting not at all.",
              }, {
                  value: "hitop_appls_3",
                  text: 'I did not feel much like eating.',
              }]
          }]
      }, {
          name: "hitop_15",
          title: "CogMood Surveys",
          elements: [{
              type: "matrix",
              name: "hitop_15",
              title: "Have there been significant times during the **last two weeks** during which the following statements applied to you?",
              isAllRowRequired: true,
              alternateRows: true,
              columnMinWidth: "83px",
              rowTitleWidth: "50%",
              columns: [{
                  value: 0,
                  text: "Not at all",
              }, {
                  value: 1,
                  text: "A little",
              }, {
                  value: 2,
                  text: "Moderately",
              }, {
                  value: 3,
                  text: "A lot",
              }],
              rows: [{
                  value: "hitop_sepinsec_8",
                  text: "I could not stand being alone.",
              }, {
                  value: "hitop_panic_6",
                  text: "I felt nauseated.",
              }]
          }]
      }, {
          name: "today_i1",
          title: "Symptoms Today",
          showQuestionNumbers: false,
          elements: [{
              type: "html",
              name: "todayintro_1",
              html: "Thank you so much for completing our surveys about your symptoms over the previous two weeks! <p><p> You're almost done with the surveys, we'd just like to find out which symptoms you've experienced <strong>today</strong>. The symptoms you are experiencing today might have more influence on how you think than other symptoms, so please review these checklists carefully. <p> <p> We have included items on the checklist that say 'Please select this item'. Please make sure to check it so that we can confirm you are reviewing the lists carefully.",
              startWithNewLine: false
          }],
      }, {
          name: "today_1",
          title: "Symptoms Today",
          elements: [{
              type: "checkbox",
              name: "today_1",
              title: "Please select the statements that apply to you **today**",
              choices: [{
                  value: "todaybaars_inattentive_1",
                  text: "Fail to give close attention to details or make careless mistakes in my work or other activities",
              }, {
                  value: "todaybaars_inattentive_2",
                  text: "Difficulty sustaining my attention in tasks or fun activities",
              }, {
                  value: "todaybaars_inattentive_3",
                  text: "Don't listen when spoken to directly",
              }, {
                  value: "todaybaars_inattentive_4",
                  text: "Don't follow through on instructions and fail to finish work or chores",
              }, {
                  value: "todaybaars_inattentive_5",
                  text: "Have difficulty organizing tasks and activities",
              }, {
                  value: "todaybaars_inattentive_6",
                  text: "Avoid, dislike, or am reluctant to engage in tasks that require sustained mental effort",
              }, {
                  value: "todaybaars_inattentive_7",
                  text: "Lose things necessary for tasks or activities",
              }, {
                  value: "todaybaars_inattentive_8",
                  text: "Easily distracted by extraneous stimuli or irrelevant thoughts",
              }, {
                  value: "todaybaars_inattentive_9",
                  text: "Forgetful in daily activities",
              }, {
                  value: "todaybaars_hyperactivity_1",
                  text: "Fidget with hands or feet or squirm in seat",
              }, {
                  value: "todaybaars_hyperactivity_2",
                  text: "Leave my seat in classrooms or in other situations in which remaining seated is expected",
              }, {
                  value: "todaybaars_hyperactivity_3",
                  text: "Shift around excessively or feel restless or hemmed in",
              }, {
                  value: "todaybaars_hyperactivity_4",
                  text: "Have difficulty engaging in leisure activities quietly (feel uncomfortable, or am loud or noisy)",
              }, {
                  value: "todaybaars_hyperactivity_5",
                  text: 'I am "on the go" or act as if "driven by a motor" (or I feel like I have to be busy or always doing something)',
              }, {
                  value: "todaybaars_impulsivity_1",
                  text: "Talk excessively (in social situations)",
              }, {
                  value: "todayattn__1",
                  text: 'Please select this item.',
              }, {
                  value: "todaybaars_impulsivity_2",
                  text: "Blurt out answers before questions have been completed, complete others' sentences, or jump the gun",
              }, {
                  value: "todaybaars_impulsivity_3",
                  text: "Have difficulty awaiting my turn",
              }, {
                  value: "todaybaars_impulsivity_4",
                  text: "Interrupt or intrude on others (butt into conversations or activities without permission or take over what others are doing)",
              }, {
                  value: "todaybaars_sct_1",
                  text: "Prone to daydreaming when I should be concentrating on something or working",
              }, {
                  value: "todaybaars_sct_2",
                  text: "Have trouble staying alert or awake in boring situations",
              }, {
                  value: "todaybaars_sct_3",
                  text: "Easily confused",
              }, {
                  value: "todaybaars_sct_4",
                  text: "Easily bored",
              }, {
                  value: "todaybaars_sct_5",
                  text: 'Spacey or "in a fog"',
              }, {
                  value: "todaybaars_sct_6",
                  text: "Lethargic, more tired than others",
              }, {
                  value: "todaybaars_sct_7",
                  text: "Underactive or have less energy than others",
              }, {
                  value: "todaybaars_sct_8",
                  text: "Slow moving",
              }, {
                  value: "todaybaars_sct_9",
                  text: "I don't seem to process information as quickly or as accurately as others",
              }, {
                  value: "today1__none",
                  text: "None of the above",
              },
              ],
              isRequired: true,
          }],
      }, {
          name: "today_2",
          title: "Symptoms Today",
          elements: [{
              type: "checkbox",
              name: "today_2",
              title: "Please select the statements that apply to you **today**",
              choices: [{
                  value: "todaygad7__1",
                  text: "Feeling nervous, anxious or on edge",
              }, {
                  value: "todaygad7__2",
                  text: "Not being able to stop or control worrying",
              }, {
                  value: "todaygad7__3",
                  text: "Worrying too much about different things",
              }, {
                  value: "todaygad7__4",
                  text: "Trouble relaxing",
              }, {
                  value: "todaygad7__5",
                  text: 'Being so restless that it is hard to sit still',
              }, {
                  value: "todaygad7__6",
                  text: "Becoming easily annoyed or irritable",
              }, {
                  value: "todaygad7__7",
                  text: "Feeling afraid, as if something awful might happen",
              }, {
                  value: "todayphq8__1",
                  text: "Little interest or pleasure in doing things",
              }, {
                  value: "todayphq8__2",
                  text: "Feeling down, depressed, irritable or hopeless",
              }, {
                  value: "todayphq8__3",
                  text: "Trouble falling or staying asleep, or sleeping too much",
              }, {
                  value: "todayphq8__4",
                  text: "Feeling tired or having little energy",
              }, {
                  value: "todayphq8__5",
                  text: 'Poor appetite or overeating',
              }, {
                  value: "todayphq8__6",
                  text: "Feeling bad about yourself – or that you are a failure or have let yourself or your family down",
              }, {
                  value: "todayphq8__7",
                  text: "Trouble concentrating on things, such as school work, reading or watching television",
              }, {
                  value: "todayphq8__8",
                  text: "Moving or speaking so slowly that other people could have noticed? Or the opposite – being so fidgety or restless that you have been moving around a lot more than usual",
              }, {
                  value: "today2__none",
                  text: "None of the above",
              }],
              isRequired: true,
          }],
      }, {
          name: "today_3",
          title: "Symptoms Today",
          elements: [{
              type: "checkbox",
              name: "today_3",
              title: "Please select the statements that apply to you **today**",
              choices: [{
                  value: "todayhitop_anhdep_1",
                  text: "I had very little energy.",
              }, {
                  value: "todayhitop_sepinsec_1",
                  text: "I worried that others would abandon me.",
              }, {
                  value: "todayhitop_anxwor_1",
                  text: "Thoughts were racing through my head.",
              }, {
                  value: "todayhitop_welbe_1",
                  text: "It was easy for me to laugh.",
              }, {
                  value: "todayhitop_appgn_1",
                  text: 'I stuffed myself with food.',
              }, {
                  value: "todayhitop_anhdep_2",
                  text: "I was unable to enjoy things like I normally do.",
              }, {
                  value: "todayhitop_sepinsec_2",
                  text: "I wanted other people to take care of me.",
              }, {
                  value: "todayhitop_anxwor_2",
                  text: "I had a lot of nervous energy.",
              }, {
                  value: "todayhitop_sepinsec_3",
                  text: "I wanted someone else to make decisions for me.",
              },  {
                  value: "todayhitop_socanx_1",
                  text: 'I avoided performing or giving a talk in front of others.',
              }, {
                  value: "todayhitop_anxwor_3",
                  text: "I was overwhelmed by anxiety.",
              }, {
                  value: "todayhitop_socanx_2",
                  text: "I avoided situations in which others were likely to watch me.",
              }, {
                  value: "todayhitop_hypsom_1",
                  text: "I felt like I could go for days without sleeping.",
              }, {
                  value: "todayhitop_anhdep_3",
                  text: "Nothing seemed interesting to me.",
              }, {
                  value: "todayhitop_cogprb_1",
                  text: 'I could not stay focused on what I was doing.',
              }, {
                  value: "todayhitop_welbe_2",
                  text: 'I looked forward to things with enjoyment.',
              }, {
                  value: "todayhitop_welbe_3",
                  text: 'I felt that I had a lot to look forward to.',
              }, {
                  value: "todayattn__2",
                  text: 'Please select this item.',
              }, {
                  value: "todayhitop_appgn_2",
                  text: "I thought a lot about food.",
              }, {
                  value: "todayhitop_sepinsec_4",
                  text: "I felt insecure about important relationships in my life.",
              }, {
                  value: "todayhitop_socanx_3",
                  text: "I felt uncomfortable being the center of attention.",
              }, {
                  value: "todayhitop_indec_1",
                  text: 'I was indecisive.',
              }, {
                  value: "todayhitop_socanx_4",
                  text: 'I felt self-conscious around others.',
              }, {
                  value: "todayhitop_appls_1",
                  text: 'My appetite was poor.',
              }, {
                  value: "todayhitop_anhdep_4",
                  text: "I felt depressed.",
              }, {
                  value: "todayhitop_appgn_3",
                  text: "I could not keep myself from eating.",
              }, {
                  value: "todayhitop_anhdep_5",
                  text: "I didn’t look forward to seeing friends or family.",
              }, {
                  value: "todayhitop_anhdep_6",
                  text: 'It took a lot of effort to do everyday activities.',
              }, {
                  value: "todayhitop_socanx_5",
                  text: 'I found it difficult to speak up in front of others.',
              }, {
                  value: "today3__none",
                  text: "None of the above",
              }],
              isRequired: true,
          }],
      }, {
          name: "today_4",
          title: "Symptoms Today",
          elements: [{
              type: "checkbox",
              name: "today_4",
              title: "Please select the statements that apply to you **today**",
              choices: [{
                  value: "todayhitop_anhdep_7",
                  text: "It felt like there wasn’t anything interesting or fun to do.",
              }, {
                  value: "todayhitop_insom_1",
                  text: "I slept very poorly.",
              }, {
                  value: "todayhitop_panic_1",
                  text: "My hands were cold or sweaty.",
              }, {
                  value: "todayhitop_indec_2",
                  text: "I had trouble making up my mind.",
              }, {
                  value: "todayhitop_welbe_4",
                  text: 'I was proud of myself.',
              }, {
                  value: "todayhitop_appls_2",
                  text: 'I lost a significant amount of weight without even trying.',
              }, {
                  value: "todayhitop_sitphb_1",
                  text: 'I avoided riding in elevators.',
              }, {
                  value: "todayhitop_anxwor_4",
                  text: "I felt tense.",
              }, {
                  value: "todayhitop_cogprb_2",
                  text: "I was easily distracted.",
              }, {
                  value: "todayhitop_socanx_6",
                  text: "I felt shy around other people.",
              }, {
                  value: "todayhitop_sepinsec_5",
                  text: 'I often felt jealous.',
              }, {
                  value: "todayhitop_anhdep_8",
                  text: 'I was a lot less talkative than usual.',
              }, {
                  value: "todayhitop_anxwor_5",
                  text: 'I worried about almost everything.',
              }, {
                  value: "todayhitop_panic_2",
                  text: "I felt dizzy or lightheaded.",
              }, {
                  value: "todayhitop_socanx_7",
                  text: "I had difficulty making eye contact with others.",
              }, {
                  value: "todayhitop_socanx_8",
                  text: 'I felt socially awkward.',
              }, {
                  value: "todayhitop_welbe_5",
                  text: 'I felt like I had a lot of interesting things to do.',
              }, {
                  value: "todayhitop_welbe_6",
                  text: 'I found compliments very encouraging.',
              }, {
                  value: "todayhitop_insom_2",
                  text: "I had trouble staying asleep.",
              }, {
                  value: "todayhitop_welbe_7",
                  text: "I felt cheerful.",
              }, {
                  value: "todayhitop_sitphb_2",
                  text: "I was afraid of flying.",
              }, {
                  value: "todayhitop_welbe_8",
                  text: 'I felt optimistic.',
              }, {
                  value: "todayhitop_welbe_9",
                  text: 'I felt like I was having a lot of fun.',
              }, {
                  value: "todayhitop_cogprb_3",
                  text: 'I had trouble remembering things.',
              }, {
                  value: "todayhitop_anhdep_9",
                  text: "I felt emotionally numb.",
              }, {
                  value: "todayhitop_welbe_10",
                  text: "I felt good about myself.",
              }, {
                  value: "todayhitop_sitphb_3",
                  text: "I was afraid of heights.",
              }, {
                  value: "todayhitop_hypsom_2",
                  text: 'I needed much less sleep than usual.',
              }, {
                  value: "todayhitop_hypsom_3",
                  text: 'I did not feel tired, even though I was sleeping less than usual.',
              }, {
                  value: "today4__none",
                  text: "None of the above",
              }],
              isRequired: true,
          }],
      }, {
          name: "today_5",
          title: "Symptoms Today",
          showQuestionNumbers: true,
          elements: [{
              type: "checkbox",
              name: "today_5",
              title: "Please select the statements that apply to you **today**",
              choices: [{
                  value: "todayhitop_anxwor_6",
                  text: 'I felt nervous and "on edge."',
              }, {
                  value: "todayhitop_socanx_9",
                  text: "I was uncomfortable entering a room when others already were present.",
              }, {
                  value: "todayhitop_indec_3",
                  text: "It was difficult for me to make decisions.",
              }, {
                  value: "todayhitop_sepinsec_6",
                  text: "I could not handle rejection.",
              }, {
                  value: "todayhitop_sitphb_4",
                  text: 'I became very anxious during a storm.',
              }, {
                  value: "todayhitop_anxwor_7",
                  text: 'I felt very stressed.',
              }, {
                  value: "todayhitop_cogprb_4",
                  text: 'I was unable to keep my mind on what I was doing.',
              }, {
                  value: "todayhitop_anhdep_10",
                  text: "Nothing made me laugh.",
              }, {
                  value: "todayhitop_appgn_4",
                  text: "I ate even when I was not really hungry.",
              }, {
                  value: "todayhitop_insom_3",
                  text: "I lay awake for a long time before falling asleep.",
              }, {
                  value: "todayhitop_sitphb_5",
                  text: 'I was afraid of the dark.',
              }, {
                  value: "todayhitop_shmglt_1",
                  text: 'I felt guilty.',
              }, {
                  value: "todayhitop_sepinsec_7",
                  text: 'I felt that I needed the approval of others.',
              }, {
                  value: "todayhitop_hypsom_4",
                  text: "I felt like I could keep going and going without ever getting tired.",
              }, {
                  value: "todayhitop_panic_3",
                  text: "I was trembling or shaking.",
              }, {
                  value: "todayhitop_socanx_10",
                  text: "I was uncomfortable meeting new people.",
              }, {
                  value: "todayhitop_panic_4",
                  text: 'My heart was racing or pounding.',
              }, {
                  value: "todayhitop_hypsom_5",
                  text: 'I never got tired.',
              }, {
                  value: "todayhitop_insom_4",
                  text: 'I woke up early and could not get back to sleep.',
              }, {
                  value: "todayhitop_shmglt_2",
                  text: "I felt ashamed of things I had done.",
              }, {
                  value: "todayhitop_panic_5",
                  text: "I was short of breath.",
              }, {
                  value: "todayhitop_shmglt_3",
                  text: 'I was disgusted with myself.',
              }, {
                  value: "todayhitop_shmglt_4",
                  text: 'I blamed myself for things.',
              }, {
                  value: "todayattn__3",
                  text: "Please select this item.",
              }, {
                  value: "todayhitop_appls_3",
                  text: 'I did not feel much like eating.',
              }, {
                  value: "todayhitop_sepinsec_8",
                  text: "I could not stand being alone.",
              }, {
                  value: "todayhitop_panic_6",
                  text: "I felt nauseated.",
              }, {
                  value: "today5__none",
                  text: "None of the above",
              }],
              isRequired: true,
          }],
      }, {
          name: "fatigue_hunger",
          title: "CogMood Surveys",
          elements: [{
              type: "radiogroup",
              name: "fatigue",
              title: "How tired do you feel right now?",
              choices: [
                  "1: Not Tired",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9: Very Tired"
              ],
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "meal_type",
              title: "By this time today, have you eaten more, less, or about the same as you usually have by this time??",
              choices: ["More", "Less", "About the same"],
              isRequired: true,
          }, {
              type: "radiogroup",
              name: "hunger",
              title: "How hungry do you feel right now?",
              choices: [
                  "1: Not hungry",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9: Very Hungry"
              ],
              isRequired: true,
          }]
      },
      ]
  }
