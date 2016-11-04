function contains(a, obj) {
    for (var i = 0; i < a.length; i++) {
        if (a[i] === obj) {
            return true;
        }
    }
    return false;
}

function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n) && n > 0;
}
$( document ).ready(function(){
	$('.submit_button').click(function(){
		$('#Error').html('')
		var values = {}
    var selected_cells = []
		var keys = ['cell-1-1','cell-1-2','cell-1-3','cell-2-1','cell-2-2','cell-2-3','cell-3-1','cell-3-2','cell-3-3']
		var flag = 0
		keys.forEach( function (arrayItem)
		{
		    var x = $('#'+arrayItem).val()
		    if(isNumber(x) != true)
		    {
		    	$('#Error').html('Please make sure all your entries are valid numbers.')
		    	flag = 1;
		    }
		    values[arrayItem] = x;
		}); 
    $('input:checked').each(function() {
        selected_cells.push($(this).attr('name'));
    });
    selected = {}
    keys.forEach( function (arrayItem)
    {
        if(contains(selected_cells,arrayItem))
        {
          selected[arrayItem] = 1
        }
        else
        {
         selected[arrayItem] = 0 
        }
    }); 
    if(flag == 0)
    {
      console.log(values);
      console.log(selected)
    }
    else
    {
      console.log("Error with values");
    }
	});
});