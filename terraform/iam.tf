
resource "google_project_iam_member" "orders_secret_accessor" {
  project = data.google_project.project.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.orders_cf_service_account.email}"
}

resource "google_project_iam_member" "orders_secret_viewer" {
  project = data.google_project.project.project_id
  role    = "roles/secretmanager.viewer"
  member  = "serviceAccount:${google_service_account.orders_cf_service_account.email}"
}

resource "google_project_iam_member" "deposit_secret_accessor" {
  project = data.google_project.project.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.deposit_cf_service_account.email}"
}

resource "google_project_iam_member" "deposit_secret_viewer" {
  project = data.google_project.project.project_id
  role    = "roles/secretmanager.viewer"
  member  = "serviceAccount:${google_service_account.deposit_cf_service_account.email}"
}
