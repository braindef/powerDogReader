<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="30">
<link rel="stylesheet" type="text/css" href="small-style.css" target="_blank">


  </head>
  <body>

   <?php

   $files = glob("*.*");

  for ($i=1; $i<count($files); $i++)

{

$image = $files[$i];
$supported_file = array(
    'gif',
    'jpg',
    'jpeg',
    'png',
    'svg'
);

$ext = strtolower(pathinfo($image, PATHINFO_EXTENSION));
if (in_array($ext, $supported_file)) {
//    print $image ."<br />";
    echo '<div><a id="'.$image .'" href="./'.$image .'"><p class=blink><b>' .$image .'</b></p></a>';
    echo '<a href="./'.$image .'"><img width=300 src="'.$image .'" ></a></div>';
    echo '
';

} else {
    continue;
 }

}

?>

