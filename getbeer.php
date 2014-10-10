<?php
$q = strval($_GET['q']);

$rcon=mysqli_connect("myhost","myuser","mypassw","mybd");
if (!$rcon) {
  die('Could not connect: ' . mysqli_error($rcon));
}
mysqli_select_db($rcon,"872251");
$sql = "select distinct beer2 from similar_beer where beer1='".$q."' order by sim_overall desc limit 1";
$result = mysqli_query($rcon,$sql);


$row = mysqli_fetch_array($result);

echo "The Beer We Recommend Is: ".$row['beer2'];
mysqli_close($rcon);
?>