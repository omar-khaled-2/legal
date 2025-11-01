# Text Extraction Queue Outputs
output "text_extraction_queue_url" {
  description = "URL of the Text Extraction SQS queue"
  value       = aws_sqs_queue.text_extraction.url
}

output "text_extraction_queue_arn" {
  description = "ARN of the Text Extraction SQS queue"
  value       = aws_sqs_queue.text_extraction.arn
}



# Text Chunking Queue Outputs
output "text_chunking_queue_url" {
  description = "URL of the Text Chunking SQS queue"
  value       = aws_sqs_queue.text_chunking.url
}

output "text_chunking_queue_arn" {
  description = "ARN of the Text Chunking SQS queue"
  value       = aws_sqs_queue.text_chunking.arn
}


# Embedding Generation Queue Outputs
output "embedding_generation_queue_url" {
  description = "URL of the Embedding Generation SQS queue"
  value       = aws_sqs_queue.embedding_generation.url
}

output "embedding_generation_queue_arn" {
  description = "ARN of the Embedding Generation SQS queue"
  value       = aws_sqs_queue.embedding_generation.arn
}



# Vector Store Insertion Queue Outputs
output "vector_store_insertion_queue_url" {
  description = "URL of the Vector Store Insertion SQS queue"
  value       = aws_sqs_queue.vector_store_insertion.url
}

output "vector_store_insertion_queue_arn" {
  description = "ARN of the Vector Store Insertion SQS queue"
  value       = aws_sqs_queue.vector_store_insertion.arn
}

# Indexed / Ready Queue Outputs
output "indexed_ready_queue_url" {
  description = "URL of the Indexed / Ready SQS queue"
  value       = aws_sqs_queue.indexed_ready.url
}

output "indexed_ready_queue_arn" {
  description = "ARN of the Indexed / Ready SQS queue"
  value       = aws_sqs_queue.indexed_ready.arn
}
