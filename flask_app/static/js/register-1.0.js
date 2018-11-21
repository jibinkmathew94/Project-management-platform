function AppViewModel() {
	self = this;
	self.email = ko.observable();
	self.name = ko.observable();
	self.password = ko.observable();
	self.confirm_password = ko.observable();
	self.emailShowLoader = ko.observable(false);
	self.empIdShowLoader = ko.observable(false);
	self.validate = function(data, event) {
		if (event.currentTarget.value) {

			if (event.currentTarget.name == 'email') {
				validator = self.emailShowLoader.bind(self);
			}
			else if (event.currentTarget.name == 'emp_id') {
				validator = self.empIdShowLoader.bind(self);
			}

			validator(true);
			console.log($(event.currentTarget).serialize());
			console.log(event.currentTarget.value);
			console.log("csrfToken is "+ csrfToken);
			$.ajax({
                type: "POST",
                url: url,
                data: $(event.currentTarget).serialize(), // serializes the form's elements.
                success: function(data) {
                	console.log(validator);
                	validator(false);
                    console.log(data)  // display the returned data in the console.
                },
                error:function(jqXhr, textStatus, errorMessage) {
                	console.log("error occured" + textStatus + " " + errorMessage);
                }
            });

            $.ajaxSetup({
            	beforeSend: function(xhr, settings) {
	                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
	                    xhr.setRequestHeader("X-CSRFToken", csrfToken)
                	}
            	}
        	})
		
		}



		
	}
}
ko.applyBindings(AppViewModel);

