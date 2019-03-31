# coding=utf-8

document="""
  <PubmedArticle>
    <MedlineCitation Status="Publisher" Owner="NLM">
      <PMID Version="1">30516272</PMID>
      <DateRevised>
        <Year>2018</Year>
        <Month>12</Month>
        <Day>05</Day>
      </DateRevised>
      <Article PubModel="Print-Electronic">
        <Journal>
          <ISSN IssnType="Electronic">1541-0420</ISSN>
          <JournalIssue CitedMedium="Internet">
            <PubDate>
              <Year>2018</Year>
              <Month>Dec</Month>
              <Day>05</Day>
            </PubDate>
          </JournalIssue>
          <Title>Biometrics</Title>
          <ISOAbbreviation>Biometrics</ISOAbbreviation>
        </Journal>
        <ArticleTitle>Linked Matrix Factorization.</ArticleTitle>
        <ELocationID EIdType="doi" ValidYN="Y">10.1111/biom.13010</ELocationID>
        <Abstract>
          <AbstractText>Several recent methods address the dimension reduction and decomposition of linked high-content data matrices. Typically, these methods consider one dimension, rows or columns, that is shared among the matrices. This shared dimension may represent common features measured for different sample sets (horizontal integration) or a common sample set with features from different platforms (vertical integration). We introduce an approach for simultaneous horizontal and vertical integration, Linked Matrix Factorization (LMF), for the general case where some matrices share rows (e.g., features) and some share columns (e.g., samples). Our motivating application is a cytotoxicity study with accompanying genomic and molecular chemical attribute data. The toxicity matrix (cell lines × chemicals) shares samples with a genotype matrix (cell lines × SNPs) and shares features with a molecular attribute matrix (chemicals × attributes). LMF gives a unified low-rank factorization of these three matrices, which allows for the decomposition of systematic variation that is shared and systematic variation that is specific to each matrix. This allows for efficient dimension reduction, exploratory visualization, and the imputation of missing data even when entire rows or columns are missing. We present theoretical results concerning the uniqueness, identifiability, and minimal parametrization of LMF, and evaluate it with extensive simulation studies. This article is protected by copyright. All rights reserved.</AbstractText>
          <CopyrightInformation>This article is protected by copyright. All rights reserved.</CopyrightInformation>
        </Abstract>
        <AuthorList CompleteYN="Y">
          <Author ValidYN="Y">
            <LastName>O'Connell</LastName>
            <ForeName>Michael J</ForeName>
            <Initials>MJ</Initials>
            <AffiliationInfo>
              <Affiliation>Department of Statistics, Miami University, Oxford, OH 45056, USA.</Affiliation>
            </AffiliationInfo>
          </Author>
          <Author ValidYN="Y">
            <LastName>Lock</LastName>
            <ForeName>Eric F</ForeName>
            <Initials>EF</Initials>
            <AffiliationInfo>
              <Affiliation>Division of Biostatistics, University of Minnesota, Minneapolis, MN 55455, USA.</Affiliation>
            </AffiliationInfo>
          </Author>
        </AuthorList>
        <Language>eng</Language>
        <PublicationTypeList>
          <PublicationType UI="D016428">Journal Article</PublicationType>
        </PublicationTypeList>
        <ArticleDate DateType="Electronic">
          <Year>2018</Year>
          <Month>12</Month>
          <Day>05</Day>
        </ArticleDate>
      </Article>
      <MedlineJournalInfo>
        <Country>United States</Country>
        <MedlineTA>Biometrics</MedlineTA>
        <NlmUniqueID>0370625</NlmUniqueID>
        <ISSNLinking>0006-341X</ISSNLinking>
      </MedlineJournalInfo>
      <KeywordList Owner="NOTNLM">
        <Keyword MajorTopicYN="N">Data integration</Keyword>
        <Keyword MajorTopicYN="N">Dimension reduction</Keyword>
        <Keyword MajorTopicYN="N">Massive data sets</Keyword>
        <Keyword MajorTopicYN="N">Missing data imputation</Keyword>
        <Keyword MajorTopicYN="N">Principal components analysis</Keyword>
      </KeywordList>
    </MedlineCitation>
    <PubmedData>
      <History>
        <PubMedPubDate PubStatus="received">
          <Year>2018</Year>
          <Month>02</Month>
          <Day>10</Day>
        </PubMedPubDate>
        <PubMedPubDate PubStatus="revised">
          <Year>2018</Year>
          <Month>08</Month>
          <Day>16</Day>
        </PubMedPubDate>
        <PubMedPubDate PubStatus="accepted">
          <Year>2018</Year>
          <Month>11</Month>
          <Day>14</Day>
        </PubMedPubDate>
        <PubMedPubDate PubStatus="entrez">
          <Year>2018</Year>
          <Month>12</Month>
          <Day>6</Day>
          <Hour>6</Hour>
          <Minute>0</Minute>
        </PubMedPubDate>
        <PubMedPubDate PubStatus="pubmed">
          <Year>2018</Year>
          <Month>12</Month>
          <Day>6</Day>
          <Hour>6</Hour>
          <Minute>0</Minute>
        </PubMedPubDate>
        <PubMedPubDate PubStatus="medline">
          <Year>2018</Year>
          <Month>12</Month>
          <Day>6</Day>
          <Hour>6</Hour>
          <Minute>0</Minute>
        </PubMedPubDate>
      </History>
      <PublicationStatus>aheadofprint</PublicationStatus>
      <ArticleIdList>
        <ArticleId IdType="pubmed">30516272</ArticleId>
        <ArticleId IdType="doi">10.1111/biom.13010</ArticleId>
      </ArticleIdList>
    </PubmedData>
  </PubmedArticle>
"""
