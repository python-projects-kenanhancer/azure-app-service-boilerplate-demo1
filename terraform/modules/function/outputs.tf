output "function_deployment_name" {
  value = google_cloudfunctions2_function.function.name
}

output "function_trigger_url" {
  value = google_cloudfunctions2_function.function.url
}

output "object_name" {
  value = google_storage_bucket_object.function_archive.name
}
