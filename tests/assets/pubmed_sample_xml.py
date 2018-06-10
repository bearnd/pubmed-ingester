# coding=utf-8

pubmed_sample_xml = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE PubmedArticleSet SYSTEM "http://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_180101.dtd">
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation Status="In-Process" Owner="NLM">
      <PMID Version="1">29144720</PMID>
      <DateRevised>
        <Year>2017</Year>
        <Month>11</Month>
        <Day>16</Day>
      </DateRevised>
      <Article PubModel="Print">
        <Journal>
          <ISSN IssnType="Electronic">1936-2692</ISSN>
          <JournalIssue CitedMedium="Internet">
            <Volume>23</Volume>
            <Issue>16 Suppl</Issue>
            <PubDate>
              <Year>2017</Year>
              <Month>Nov</Month>
            </PubDate>
          </JournalIssue>
          <Title>The American journal of managed care</Title>
          <ISOAbbreviation>Am J Manag Care</ISOAbbreviation>
        </Journal>
        <ArticleTitle>Cost-effectiveness of gammaCore (non-invasive vagus nerve stimulation) for acute treatment of episodic cluster headache.</ArticleTitle>
        <Pagination>
          <MedlinePgn>S300-S306</MedlinePgn>
        </Pagination>
        <Abstract>
          <AbstractText>Cluster headache is a debilitating disease characterized by excruciatingly painful attacks that affects 0.15% to 0.4% of the US population. Episodic cluster headache manifests as circadian and circannual seasonal bouts of attacks, each lasting 15 to 180 minutes, with periods of remission. In chronic cluster headache, the attacks occur throughout the year with no periods of remission. While existing treatments are effective for some patients, many patients continue to suffer. There are only 2 FDA-approved medications for episodic cluster headache in the United States, while others, such as high-flow oxygen, are used off-label. Episodic cluster headache is associated with comorbidities and affects work, productivity, and daily functioning. The economic burden of episodic cluster headache is considerable, costing more than twice that of nonheadache patients. gammaCore adjunct to standard of care (SoC) was found to have superior efficacy in treatment of acute episodic cluster headaches compared with sham-gammaCore used with SoC in ACT1 and ACT2 trials. However, the economic impact has not been characterized for this indication. We conducted a cost-effectiveness analysis of gammaCore adjunct to SoC compared with SoC alone for the treatment of acute pain associated with episodic cluster headache attacks. The model structure was based on treatment of acute attacks with 3 outcomes: failures, nonresponders, and responders. The time horizon of the model is 1 year using a payer perspective with uncertainty incorporated. Parameter inputs were derived from primary data from the randomized controlled trials for gammaCore. The mean annual costs associated with the gammaCore-plus-SoC arm was $9510, and mean costs for the SoC-alone arm was $10,040. The mean quality-adjusted life years for gammaCore-plus-SoC arm were 0.83, and for the SoC-alone arm, they were 0.74. The gammaCore-plus-SoC arm was dominant over SoC alone. All 1-way and multiway sensitivity analyses were cost-effective using a threshold of $20,000. gammaCore dominance, representing savings, was driven by superior efficacy, improvement in quality of life (QoL), and reduction in costs associated with successful and consistent abortion of episodic attacks. These findings serve as additional economic evidence to support coverage for gammaCore. Additional real-world data are needed to characterize the long-term impact of gammaCore on comorbidities, utilization, QoL, daily functioning, productivity, and social engagement of these patients, and for other indications.</AbstractText>
        </Abstract>
        <AuthorList CompleteYN="Y">
          <Author ValidYN="Y">
            <LastName>Mwamburi</LastName>
            <ForeName>Mkaya</ForeName>
            <Initials>M</Initials>
          </Author>
          <Author ValidYN="Y">
            <LastName>Liebler</LastName>
            <ForeName>Eric J</ForeName>
            <Initials>EJ</Initials>
          </Author>
          <Author ValidYN="Y">
            <LastName>Tenaglia</LastName>
            <ForeName>Andrew T</ForeName>
            <Initials>AT</Initials>
          </Author>
        </AuthorList>
        <Language>eng</Language>
        <PublicationTypeList>
          <PublicationType UI="D016428">Journal Article</PublicationType>
        </PublicationTypeList>
      </Article>
      <MedlineJournalInfo>
        <Country>United States</Country>
        <MedlineTA>Am J Manag Care</MedlineTA>
        <NlmUniqueID>9613960</NlmUniqueID>
        <ISSNLinking>1088-0224</ISSNLinking>
      </MedlineJournalInfo>
    </MedlineCitation>
    <PubmedData>
      <History>
        <PubMedPubDate PubStatus="entrez">
          <Year>2017</Year>
          <Month>11</Month>
          <Day>17</Day>
          <Hour>6</Hour>
          <Minute>0</Minute>
        </PubMedPubDate>
        <PubMedPubDate PubStatus="pubmed">
          <Year>2017</Year>
          <Month>11</Month>
          <Day>17</Day>
          <Hour>6</Hour>
          <Minute>0</Minute>
        </PubMedPubDate>
        <PubMedPubDate PubStatus="medline">
          <Year>2017</Year>
          <Month>11</Month>
          <Day>17</Day>
          <Hour>6</Hour>
          <Minute>0</Minute>
        </PubMedPubDate>
      </History>
      <PublicationStatus>ppublish</PublicationStatus>
      <ArticleIdList>
        <ArticleId IdType="pubmed">29144720</ArticleId>
        <ArticleId IdType="pii">87325</ArticleId>
      </ArticleIdList>
    </PubmedData>
  </PubmedArticle>
</PubmedArticleSet>
"""
