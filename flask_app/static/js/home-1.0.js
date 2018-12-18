let homeViewModel = function(){
	this.projectsActive = ko.observable(false);
	this.featuresActive = ko.observable(true);
	this.showFeaturesTab = function(){
		this.projectsActive(false);
		this.featuresActive(true);
	}
	this.showProjectsTab = function(){
		this.featuresActive(false);
		this.projectsActive(true);
	}
}

ko.bindingHandlers.switchTabsFade = {

    update: function(element, valueAccessor) {
        // Whenever the value subsequently changes, slowly fade the element in or out
        var value = valueAccessor();
        console.log(ko.unwrap(value))
        ko.unwrap(value) ? $(element).fadeIn() : $(element).hide();
        console.log(element);
    }
};

ko.applyBindings(homeViewModel);