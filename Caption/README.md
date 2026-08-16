# Image Captioning Using BLIP-2

A Django-based image captioning application integrating a BLIP-2 vision-language model
with blockchain-based data storage.

## Main Components

- Django web application
- BLIP-2 image captioning
- SQLite/Django data layer
- Ethereum/Ganache smart-contract integration
- Solidity smart contract in `blocks/contracts/`

## Project Structure

- `App/` - application code
- `Caption/` - Django project configuration
- `blocks/` - blockchain smart contract and configuration
- `templates/` - web templates
- `static/` - static assets
- `manage.py` - Django entry point
- `req.txt` - Python dependencies

## Important

Create your own environment variables for secrets and local blockchain configuration.
Do not commit passwords, private keys, `.env`, databases, or generated build artifacts.
