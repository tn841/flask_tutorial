#-*- coding:utf-8 -*-
import sys

from flask.templating import render_template

from photolog import create_app

reload(sys)
sys.setdefaultencoding('utf-8')

app = create_app()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('/404.html'), 404

if __name__ == '__main__':
    print "starting test server"
    app.run(port=2323, debug=True)