<?php
$myfile = fopen("/Users/hu/Desktop/project/learnphp/server/python-cli/1.txt", "w") or die("Unable to open file!");
$data = $_POST['field1']."\r\n";
fwrite($myfile, $data);
//fwrite($myfile, $data);
fclose($myfile);

$myfile2 = fopen("/Users/hu/Desktop/project/learnphp/server/python-cli/2.txt", "w") or die("Unable to open file!");
$data2 = $_POST['field2']."\r\n";
fwrite($myfile2, $data2);
//fwrite($myfile2, $data2);
fclose($myfile2);
?>