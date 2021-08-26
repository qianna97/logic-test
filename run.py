from webapp import app
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process')
	parser.add_argument('process', type=str, help='directory')
	args = parser.parse_args()

	if args.process == 'runserver':
		app.run(host="0.0.0.0", debug=True)
	elif args.process == 'migrate':
		from webapp import db
		db.drop_all()
		db.create_all()
		db.session.commit()