Keyword Libraries
=============== 

Goals of Care
^^^^^^^^^^^^^

**Definition**

Conversations with patients or family members about the patient’s goals, values, or priorities for treatment and outcomes. Includes statements that conversation occurred as well as listing specific goals.

*OR*

Advance care planning was discussed, reviewed, recommended, or completed.

**Original key words**

goc, goals of care, goals for care, goals of treatment, goals for treatment, treatment goals, family meeting, family discussion, family discussions, patient goals, patient values, quality of life, prognostic discussions, illness understanding, serious illness conversation, serious illness discussion, acp, advance care planning, advanced care planning

**Key words added at Mayo**

Supportive care, comfort care, comfort approach, comfort directed care, advanced care plan/goals of care, comfort measures, end of life care

**Key words added at Duke**

wish

**Key words added at Northwell**

advance care plan, what matters most

**Final Regex Used**

goc, goals? (of|for) (care|treatment), treatment goals?, family (meeting|discussions?), patient (goals?|values?), quality of life, prognostic discussions?, illness understanding, serious illness (conversation|discussion), acp, advanced? care plan(ing)?(?!\s* \nfull code), supportive care, comfort( directed)? care, comfort approach, advanced care plan/goals of care, comfort measures, end of life care, what matters most, (?<! your primary care doctor may) wish(?! you)

Palliative Care
^^^^^^^^^^^^^

**Definition**

Documentation that specialist palliative care was discussed, patient preferences regarding seeing palliative care clinician.

**Original key words**

palliative care, palliative medicine, pall care, pallcare, palcare, supportive care

**Key words added at Mayo**

Mayo recommended removing supportive care

**Key words added at Duke**

N/A

**Key words added at Northwell**

N/A

**Final Regex Used**

pall(iative)? (care|medicine), pall?care

Hospice
^^^^^^^^^^^^^

**Definition**

Documentation that hospice was discussed, prior enrollment in hospice, patient preferences regarding hospice, or assessments the patient did not meet hospice criteria.

**Original key words**

hospice

**Key words added at Mayo**

N/A

**Key words added at Duke**

DNAR

**Key words added at Northwell**

N/A

**Final Regex Used**

hospice

Code Status Limitations
^^^^^^^^^^^^^

**Definition**

Conversations with patients or family members about preferences for limitations to cardiopulmonay resuscitation and intubation.

**Original key words**

dnr, dnrdni, dni, dnr/dni, do not resuscitate, do-not-resuscitate, do not intubate, do-not-intubate, no intubation, no mechanical ventilation, no ventilation, no CPR, declines CPR, no cardiopulmonary resuscitation, chest compressions, no defibrillation, no dialysis, no NIPPV, no bipap, no endotracheal intubation, no mechanical intubation, declines dialysis, refuses dialysis, shocks, cmo, comfort measures, comfort, comfort care

**Key words added at Mayo**

do not resuscitate/do not intubate, DNR/DNI/DNH, DNR/I

**Key words added at Duke**

N/A

**Key words added at Northwell**

DNR/I

**Final Regex Used**

dn(r|i)/?dn(i|r), do( |-)not( |-)(resuscitate|intubate), no (mechanical)? intubation, no (mechanical)? ventilation, (no|declines?) CPR, no cardiopulmonary resuscitation, chest compressions, no defibrillation, no dialysis, no NIPPV, no bipap, no endotracheal intubation, declines? dialysis, refuses? dialysis, shocks, cmo, comfort (measures|care), do not resuscitate/do not intubate, DNR/DNI/DNH, DNR/I, DNAR
