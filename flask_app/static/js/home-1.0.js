$.ajaxSetup({
            	beforeSend: function(xhr, settings) {
	                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
	                    xhr.setRequestHeader("X-CSRFToken", csrfToken);
                	}
            	}
        	});


let homeViewModel = function(){
	let self = this;
	this.projectsActive = ko.observable(false);
	this.featuresActive = ko.observable(true);
	this.showFeaturesTab = function(){
		this.projectsActive(false);
		this.featuresActive(true);
	};
	this.showProjectsTab = function(){
		this.featuresActive(false);
		this.projectsActive(true);
	};
	this.features = ko.observableArray();
	this.projects = ko.observableArray();
	this.getData = function(){
		$.ajax({
		type: "POST",
		url: '/features',
		success: function(data) {
			console.log(data);
			for(var i in data){
				self.features.push(data[i])
			 // display the returned data in the console.
			}
		},
		error:function(jqXhr, textStatus, errorMessage) {
			console.log("error occured" + textStatus + " " + errorMessage);
			}
	});
	}
	this.getData();
};


ko.components.register('feature-card', {
    template: {element: 'feature-card-template'},
});


ko.bindingHandlers.switchTabsFade = {

    update: function(element, valueAccessor) {
        // Whenever the value subsequently changes, slowly fade the element in or out
        var value = valueAccessor();
        console.log(ko.unwrap(value));
        ko.unwrap(value) ? $(element).fadeIn() : $(element).hide();
        console.log(element);
    }
};

ko.applyBindings(homeViewModel);