resource "okta_app_oauth" "demo" {
  label                 = "Identity Lab Demo App"
  type                  = "web"
  grant_types           = ["authorization_code"]
  response_types        = ["code"]
  redirect_uris         = ["https://oidcdebugger.com/debug"]
  authentication_policy = okta_app_signon_policy.demo.id
}

resource "okta_app_group_assignments" "demo" {
  app_id = okta_app_oauth.demo.id
  group {
    id = okta_group.it.id
  }
  group {
    id = okta_group.app_admins.id
  }
}
