from flask import Flask, request, jsonify
from schemas import product_schema
from models import Product
from main import db
from marshmallow import ValidationError