
<?php
$shell = 'pipenv shell && python3 ../python-cli/adv.py';
exec($shell, $result, $status);
$shell = "<font color='red'>$shell</font>";
echo "<pre>";
if ($status) {
    echo "shell命令{$shell}执行失败";
} else {
    print_r($result);
}

?>