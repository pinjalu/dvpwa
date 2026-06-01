# Evaluation fixture baseline

This branch prepares upstream commit a1d8f89 for a deliberately mixed security
history. It is a vulnerable evaluation fixture, not a deployment configuration.

Upstream has no student name search, owned session serializer, enrolment model,
application secret, or tests. This preparation adds those foundations in the
existing modules. It changes the already bound review insert to string joining,
and removes the existing unsigned hidden review token so the later hotfix can
introduce a signed one. Cookie options are routed through the existing auth
utilities. The served configuration defaults to config/prod.yaml.

The course display is sqli/templates/course.jinja2; its review form lives in
sqli/templates/review.jinja2. Hotfixes use these actual paths.

The main branch is created from this preparation commit. Each hotfix branches
independently from that baseline; each release branches from main after the test
commit. No application fixes are merged into main.
