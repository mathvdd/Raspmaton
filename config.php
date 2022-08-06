<!DOCTYPE html>
<html>
<title>Config page</title>
<body style="background-image: linear-gradient(to right, violet , orange);">
<h1>Configuration</h1>

<!-- event name configuration -->
<?php

  $fileevent = "./fold_name.conf";

  // rewrite the config file
  if(isset($_POST['SubmitButton'])){ //check if form was submitted
    $input = $_POST['inputText']; //get input text
    if(!isset($input) || trim($input) == ''){ //change to 'noname' if input is empty and not spaces
      $input = "noname";
    }
    $file = fopen($fileevent, "w") or die("Unable to open file!"); //write the file
    fwrite($file, $input);
    fclose($file);

  }

  // open config file and read the content
   $fileread = fopen( $fileevent, "r" );

   if( $fileread == false ) {
      echo ( "Error in opening file" );
      exit();
   }

   $filesize = filesize( $fileevent );
   $filetext = fread( $fileread, $filesize );
   fclose( $fileread );

    echo "<h2>Update the picture folder</h2>";
    echo "Will only work if the raspberry can connect to the internet, at boot<br>";
    echo "By default is 'noname'<br><br>";
    echo ( "Current folder name: <b>$filetext</b><br><br>" );
?>

<form action="" method="post">
  <label for="fname">Folder name:</label>
  <input type="text" name="inputText"/>
  <input type="submit" name="SubmitButton" value="Update"/>
</form>


<!-- git update configuration -->
<?php

  $filegitup = "./git_update.conf";

  // rewrite the config file
  if(isset($_POST['UpdateOn'])){
    $gitupstate = "On";
    $file = fopen($filegitup, "w") or die("Unable to open file!"); //write the file
    fwrite($file, $gitupstate);
    fclose($file);
    }
  if(isset($_POST['UpdateOff'])){
    $gitupstate = "Off";
    $file = fopen($filegitup, "w") or die("Unable to open file!"); //write the file
    fwrite($file, $gitupstate);
    fclose($file);
    }
  // open config file and read the content

   $handle = fopen( $filegitup, "r" );
   // echo $handle

   if( $handle == false ) {
      echo ( "Error in opening file" );
      exit();
   }

   $filesizeg = filesize( $filegitup );
   $filetextg = fread( $handle, $filesizeg );
   fclose( $handle );

    echo "<h2>Git update</h2>";
    echo "Will only work if the raspberry can connect to the internet, at boot<br>";
    echo "Will reboot automatically and set update to off<br>";
    echo ( "Current configuration: <b>$filetextg</b><br><br>" );
?>
<form action="" method="post">
  <input type="submit" name="UpdateOn" value="Update from Github"/>
  <input type="submit" name="UpdateOff" value="Cancel update"/>
</form>

</body>
</html>
