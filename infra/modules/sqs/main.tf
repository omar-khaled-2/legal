# SQS Queue for Text Extraction Stage
resource "aws_sqs_queue" "text_extraction" {
  name                       = "${var.environment}-text-extraction-queue"
  delay_seconds              = 0
  max_message_size           = 262144 # 256 KB
  message_retention_seconds  = 1209600 # 14 days
  receive_wait_time_seconds  = 20
  visibility_timeout_seconds = 300 # 5 minutes

  tags = {
    Name        = "${var.environment}-text-extraction-queue"
    Environment = var.environment
    Stage       = "text-extraction"
  }
}

# SQS Queue for Text Chunking Stage
resource "aws_sqs_queue" "text_chunking" {
  name                       = "${var.environment}-text-chunking-queue"
  delay_seconds              = 0
  max_message_size           = 262144 # 256 KB
  message_retention_seconds  = 1209600 # 14 days
  receive_wait_time_seconds  = 20
  visibility_timeout_seconds = 300 # 5 minutes

  tags = {
    Name        = "${var.environment}-text-chunking-queue"
    Environment = var.environment
    Stage       = "text-chunking"
  }
}

# SQS Queue for Embedding Generation Stage
resource "aws_sqs_queue" "embedding_generation" {
  name                       = "${var.environment}-embedding-generation-queue"
  delay_seconds              = 0
  max_message_size           = 262144 # 256 KB
  message_retention_seconds  = 1209600 # 14 days
  receive_wait_time_seconds  = 20
  visibility_timeout_seconds = 300 # 5 minutes

  tags = {
    Name        = "${var.environment}-embedding-generation-queue"
    Environment = var.environment
    Stage       = "embedding-generation"
  }
}

# SQS Queue for Vector Store Insertion Stage
resource "aws_sqs_queue" "vector_store_insertion" {
  name                       = "${var.environment}-vector-store-insertion-queue"
  delay_seconds              = 0
  max_message_size           = 262144 # 256 KB
  message_retention_seconds  = 1209600 # 14 days
  receive_wait_time_seconds  = 20
  visibility_timeout_seconds = 300 # 5 minutes

  tags = {
    Name        = "${var.environment}-vector-store-insertion-queue"
    Environment = var.environment
    Stage       = "vector-store-insertion"
  }
}

# SQS Queue for Indexed / Ready Stage
resource "aws_sqs_queue" "indexed_ready" {
  name                       = "${var.environment}-indexed-ready-queue"
  delay_seconds              = 0
  max_message_size           = 262144 # 256 KB
  message_retention_seconds  = 1209600 # 14 days
  receive_wait_time_seconds  = 20
  visibility_timeout_seconds = 300 # 5 minutes

  tags = {
    Name        = "${var.environment}-indexed-ready-queue"
    Environment = var.environment
    Stage       = "indexed-ready"
  }
}

