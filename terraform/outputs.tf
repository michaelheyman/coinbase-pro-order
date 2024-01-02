output "orders_function_url" {
  # Access the module output with module.<module_name>.<output_name>
  value = module.orders_function.function_url
}

output "deposit_function_url" {
  # Access the module output with module.<module_name>.<output_name>
  value = module.deposit_function.function_url
}
