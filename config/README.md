# Configuration Directory

This directory contains configuration files for the Manga Metadata Fixer application.

## Overview

Place any configuration files here (YAML, JSON, etc.) for advanced usage or future extensions.

## Configuration Options

### Environment-based Configuration

The application primarily uses environment variables for configuration. See the main README.md for details.

### File-based Configuration (Future)

Future versions may support configuration files for:

- **API endpoint mappings** - Custom mapping between metadata fields
- **Batch processing rules** - Automated processing configurations  
- **Metadata validation schemas** - Custom validation rules
- **Logging configurations** - Advanced logging setups
- **Rate limiting settings** - API throttling configurations

### Example Configuration Files

#### `metadata_mapping.yml` (Future feature)
```yaml
komga:
  title_field: "title"
  description_field: "summary" 
  status_mapping:
    ongoing: "ONGOING"
    completed: "ENDED"
    hiatus: "HIATUS"

kavita:
  title_field: "name"
  description_field: "summary"
  status_mapping:
    ongoing: "OnGoing"
    completed: "Completed"
    hiatus: "Hiatus"
```

#### `processing_rules.yml` (Future feature)
```yaml
batch_processing:
  max_concurrent_requests: 5
  retry_attempts: 3
  retry_delay: 1000  # milliseconds
  
validation:
  required_fields: ["title", "summary"]
  max_title_length: 200
  max_summary_length: 2000
```

## Security Notes

- **Never commit sensitive data** like API tokens to this directory
- Use `.env` files or environment variables for secrets
- Configuration files in this directory are included in `.gitignore` patterns for common sensitive extensions (`.json`, `.yml`, `.yaml`, `.ini`, `.conf`)

## Adding Configuration Files

1. Create your configuration file in this directory
2. Update the application code to read the configuration
3. Document the configuration options in this README
4. Add appropriate `.gitignore` patterns if the config contains sensitive data

## Current Status

Currently, the application uses environment variables for all configuration. File-based configuration support may be added in future versions based on user needs.