==============================================
OAuth 2.0 Client Credentials Plugin for HTTPie
==============================================

This is a quick HTTPie plugin to allow quick testing if Resource Server applications using an OAuth 2.0 Client Credentials flow.

Install:
========

This module is still early in development, clone the repo and install:

   ::
      python setup.py install

Usage:
======

   ::
      http --auth-type oauth2 \
           --auth client-id:client-secret \ 
           --issuer-uri "https://issuer.example.com/oauth/token" \
           --scope your-scope-here \
         GET localhost:8080/your-url-here
