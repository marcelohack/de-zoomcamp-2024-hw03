terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

data "google_storage_bucket" "bucket" {
  name = "${var.project}-${var.gcs_bucket_name}"
}

data "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
}

resource "google_bigquery_table" "external" {
  dataset_id = data.google_bigquery_dataset.dataset.dataset_id
  table_id   = "${local.table_prefix}_external"
  deletion_protection = false

  external_data_configuration {
    source_format = "PARQUET"
    autodetect    = true

    source_uris = [
      "gs://${data.google_storage_bucket.bucket.name}/${local.object_key_prefix}/*.parquet",
    ]
  }
}

