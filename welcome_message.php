<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Welcome to CodeIgniter</title>

	<style type="text/css">

	::selection{ background-color: #E13300; color: white; }
	::moz-selection{ background-color: #E13300; color: white; }
	::webkit-selection{ background-color: #E13300; color: white; }

	body {
		background-color: #fff;
		margin: 40px;
		font: 13px/20px normal Helvetica, Arial, sans-serif;
		color: #4F5155;
	}

	a {
		color: #003399;
		background-color: transparent;
		font-weight: normal;
	}

	h1 {
		color: #444;
		background-color: transparent;
		border-bottom: 1px solid #D0D0D0;
		font-size: 19px;
		font-weight: normal;
		margin: 0 0 14px 0;
		padding: 14px 15px 10px 15px;
	}

	code {
		font-family: Consolas, Monaco, Courier New, Courier, monospace;
		font-size: 12px;
		background-color: #f9f9f9;
		border: 1px solid #D0D0D0;
		color: #002166;
		display: block;
		margin: 14px 0 14px 0;
		padding: 12px 10px 12px 10px;
	}

	#body{
		margin: 0 15px 0 15px;
	}
	
	p.footer{
		text-align: right;
		font-size: 11px;
		border-top: 1px solid #D0D0D0;
		line-height: 32px;
		padding: 0 10px 0 10px;
		margin: 20px 0 0 0;
	}
	
	#container{
		margin: 10px;
		border: 1px solid #D0D0D0;
		-webkit-box-shadow: 0 0 8px #D0D0D0;
	}
	</style>

	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
	<script>
	function showBeer() {
                        var e = document.getElementById("Blist");
                        var str = e.options[e.selectedIndex].text;
			if (str=="") {
			document.getElementById("rcmd").innerHTML="";
			return;
			} 
			if (window.XMLHttpRequest) {
			// code for IE7+, Firefox, Chrome, Opera, Safari
			xmlhttp=new XMLHttpRequest();
			} 
			else { // code for IE6, IE5
			xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
			}
			xmlhttp.onreadystatechange=function() {
				if (xmlhttp.readyState==4 && xmlhttp.status==200) {
					document.getElementById("rcmd").innerHTML=xmlhttp.responseText;
				}
			}
			xmlhttp.open("GET","getbeer.php?q="+str,true);
			xmlhttp.send();
		};
	</script>
</head>
<body>

<div id="container">
	<h1>Welcome to BeeRecomand!</h1>	
	<div id="body">
		<p>Select Your Favourite Beer.</p>
        <form name="f1" action='javascript'>
		<select id='Blist'>
		<?php
		$con=mysqli_connect("myhost","myuser","mypassw","mybd");
		$sql = 'select distinct beer1 from similar_beer order by beer1';
		$res = mysqli_query($con,$sql);
		while($row = mysqli_fetch_array($res)) {
			$fav=$row["beer1"];
			echo "<option value=".$fav.">".$fav."</option>";
		}
		mysqli_close($con);
		?>
		</select>   
		</form>       
		<div id="rcmd">The Beer We Recommend Is: </div>
		<button   onclick="showBeer()" id="btn" ">Beer!</button>  
		
	</div>
	

  <!-- <p class="footer">Page rendered in <strong>{elapsed_time}</strong> seconds</p> -->
</div>

</body>
</html>			