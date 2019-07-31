<?php

$file = fopen("/Users/hu/Desktop/project/learnphp/server/python-cli/output.txt", "r") or exit("Unable to open file!");
//Output a line of the file until the end is reached
while (!feof($file)) {
    echo fgets($file) . "<br>";
}
fclose($file);


//
//$fn = fopen("output.txt", "r");
//
//while (!feof($fn)) {
//    $result = fgets($fn);
//    echo $result;
//}
//
//fclose($fn);


///*
//* read txt file
//*/
//function getTxtcontent($txtfile)
//{
//    $file = fopen("output.txt", "r");
//    $content = array();
//    if (!$file) {
//        return 'fail to open the file';
//    } else {
//        $i = 0;
//        while (!feof($file)) {
//            $content[$i] = mb_convert_encoding(fgets($file), "UTF-8", "GBK,ASCII,ANSI,UTF-8");
//            $i++;
//        }
//        fclose($file);
//        $content = array_filter($content);
//    }
//
//    return $content;
//}
?>