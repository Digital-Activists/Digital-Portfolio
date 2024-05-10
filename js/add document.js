var dt = new DataTransfer();
 
$('.input-doc input[type=file]').on('change', function(){
	let $files_list = $(this).closest('.input-doc').next();
	$files_list.empty();
 

	for(var i = 0; i < this.files.length; i++){
		let file = this.files.item(i);
		dt.items.add(file);    
   
		let reader = new FileReader();
		reader.readAsDataURL(file);
		reader.onloadend = function(){
			let new_file_input =   '<div class="input-doc-list-item">' + 
            '<img src="/images/file.png" class="file">' + 
				'<span class="input-doc-list-name">' + file.name + '</span>' +
				'<a href="#" onclick="removeDocsItem(this); return false;" class="input-doc-list-remove">x</a>' +
			'</div>';
			$files_list.append(new_file_input); 
		}
	};
	this.files = dt.files;
});
 
function removeDocsItem(target){
	let name = $(target).prev().text();
	let input = $(target).closest('.input-doc-row').find('input[type=file]');	
	$(target).closest('.input-doc-list-item').remove();	
	for(let i = 0; i < dt.items.length; i++){
		if(name === dt.items[i].getAsFile().name){
			dt.items.remove(i);
		}
	}
	input[0].files = dt.files;  
}