<?xml version="1.0" encoding="UTF-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2">
  <title>PayPal DITA Documentation Standards</title>

  <!-- Rule 1: Every topic must have a shortdesc -->
  <pattern id="shortdesc-required">
    <rule context="concept | task | reference">
      <assert test="shortdesc" role="warning">
        Topics must include a shortdesc for search snippets and WebHelp hover previews.
      </assert>
    </rule>
  </pattern>

  <!-- Rule 2: Topic @id must use lowercase kebab-case -->
  <pattern id="topic-id-convention">
    <rule context="concept | task | reference | topic">
      <assert test="matches(@id, '^[a-z][a-z0-9\-]+$')" role="error">
        Topic @id must use lowercase kebab-case (e.g., "create-order" not "CreateOrder").
      </assert>
    </rule>
  </pattern>

  <!-- Rule 3: API codeblocks must start with HTTP method -->
  <pattern id="api-codeblock-method">
    <rule context="codeblock[contains(., '/v1/') or contains(., '/v2/')]">
      <assert test="matches(normalize-space(.), '^(GET|POST|PUT|PATCH|DELETE|curl)')"
              role="warning">
        Codeblocks showing PayPal API calls should start with the HTTP method or 'curl'.
      </assert>
    </rule>
  </pattern>

  <!-- Rule 4: Tasks must have at least 2 steps -->
  <pattern id="task-min-steps">
    <rule context="taskbody/steps">
      <assert test="count(step) >= 2" role="warning">
        A task with only one step may be better as a note inside a concept topic.
      </assert>
    </rule>
  </pattern>

  <!-- Rule 5: Tables must have a title -->
  <pattern id="table-title-required">
    <rule context="table">
      <assert test="title" role="warning">
        Tables should include a title element for accessibility and PDF labeling.
      </assert>
    </rule>
  </pattern>

  <!-- Rule 6: Steps must have a cmd child -->
  <pattern id="step-cmd-required">
    <rule context="step">
      <assert test="cmd" role="error">
        Every step must contain a cmd element with the instruction text.
      </assert>
    </rule>
  </pattern>

</schema>
