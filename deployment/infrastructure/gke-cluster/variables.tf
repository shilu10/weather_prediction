variable "project_id" {
    type = string
}

variable "cluster_name" {
    type = string
}

variable "region" {
    type = string
}

variable "location" {
    type = string
}

variable "google_access_token"{
    type = string
    sensitive = true
}
