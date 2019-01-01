$.ajaxSetup({
            	beforeSend: function(xhr, settings) {
	                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
	                    xhr.setRequestHeader("X-CSRFToken", csrfToken);
                	}
            	}
        	});

let accountViewModel = function(){
	this.updatePicture = function(data, event){
		console.log('chakka');
		fd = new FormData();
		fd.append('picture', event.currentTarget.files[0]);
		for (var pair of fd.entries()) {
    		console.log(pair[0]+ ', ' + pair[1]); 
		}
		$.ajax({
        // Your server script to process the upload
        url: 'update-image',
        type: 'POST',

        // Form data
        data: fd,

        // Tell jQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false,

        // Custom XMLHttpRequest
        xhr: function() {
            var myXhr = $.ajaxSettings.xhr();
            if (myXhr.upload) {
                // For handling the progress of the upload
                myXhr.upload.addEventListener('progress', function(e) {
                    if (e.lengthComputable) {
                        $('progress').attr({
                            value: e.loaded,
                            max: e.total,
                        });
                    }
                } , false);
            }
            return myXhr;
        },

        success: function(data) {
			$("img").attr("src",data);
		},
    });
	};
};

ko.applyBindings(accountViewModel);