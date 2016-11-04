var keys = ['cell-1-1','cell-1-2','cell-1-3','cell-2-1','cell-2-2','cell-2-3','cell-3-1','cell-3-2','cell-3-3'];
function isNumber(n) {
  return !isNaN(parseFloat(n)) && isFinite(n) && n > 0;
}
function displayList(list_of_values)
{
	var i = 0
	keys.forEach( function (arrayItem)
	{
		$('#'+arrayItem+'-value').html(list_of_values[i])
		i = i + 1
	});
}

$( document ).ready(function(){
	displayList([1,2,3,4,5,6,7,8,9]);
	$('.submit_button').click(function(){
		$('#Error').html('')
		var values = {}
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
		if(flag == 0)
		{
			console.log(values);
		}
		else
		{
			console.log("Error with values");
		}
	});
});