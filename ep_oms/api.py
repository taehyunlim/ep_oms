import easypost
from ep_oms import application, db
easypost.api_key = application.config['EP_API_KEY']

def ep_to_address(form):
	to_address = easypost.Address.create(
		verify=["delivery"],
		name=form.name.data,
		street1=form.street1.data,
		street2=form.street2.data,
		city=form.city.data,
		state=form.state.data,
		zip=form.zip.data,
		country="US"
	)
	return to_address.id
