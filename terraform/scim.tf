# The app was created in the Admin Console (SCIM can't be switched on in
# Terraform for custom apps). Terraform manages who gets it.
data "okta_app" "scim" {
  label = "SCIM Playground"
}

resource "okta_app_group_assignments" "scim" {
  app_id = data.okta_app.scim.id

  group {
    id = okta_group.it.id
  }
  group {
    id = okta_group.finance.id
  }
}
