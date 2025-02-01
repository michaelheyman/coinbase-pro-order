resource "google_service_account" "orders_cf_service_account" {
  account_id   = "orders-cf-sa"
  display_name = "Orders Cloud Function Service Account"
  project      = data.google_project.project.project_id
}

resource "google_service_account" "deposit_cf_service_account" {
  account_id   = "deposit-cf-sa"
  display_name = "Deposit Cloud Function Service Account"
  project      = data.google_project.project.project_id
}
