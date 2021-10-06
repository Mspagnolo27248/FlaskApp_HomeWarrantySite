from project_files import db
from project_files.models import User,TicketModel,CategoryModel
from sqlalchemy import create_engine
db.create_all()

#db.CategoryModel.add(['Roof','Landscaping','Electric','Plumbing','Trim','Paint','Flooring'])

# categories = ['Roof','Landscaping','Electric','Plumbing','Trim','Paint','Flooring']
# cat_models = []
# for cat in categories:
#     cat_models.append(CategoryModel(cat))

query = \
"""
insert into category
values 
(1,'Flooring'),
(2,'Landscaping'),
(3,'Electric'),
(4,'Plumbing'),
(5,'Paint'),
(6,'Trim'),
(7,'Roof'),
(8,'Doors'),
(9,'Siding'),
(10,'Kitchen'),
(11,'Bathroom'),
(12,'HVAC')

"""
db.session.execute(query)
db.session.commit()