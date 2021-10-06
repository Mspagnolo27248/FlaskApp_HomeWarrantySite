from project_files import db
from project_files.models import User,TicketModel,CategoryModel
from sqlalchemy import create_engine
db.create_all()

#db.CategoryModel.add(['Roof','Landscaping','Electric','Plumbing','Trim','Paint','Flooring'])

categories = ['Roof','Landscaping','Electric','Plumbing','Trim','Paint','Flooring']
cat_models = []
for cat in categories:
    cat_models.append(CategoryModel(cat))

db.session.add(cat_models)
db.session.commit()