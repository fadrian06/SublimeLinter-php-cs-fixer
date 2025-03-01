<?php

use PhpCsFixer\Config;
use PhpCsFixer\Finder;
use PhpCsFixer\Runner\Parallel\ParallelConfigFactory;

$finder = Finder::create()->in(__DIR__);

$config = new Config;

return $config
  ->setParallelConfig(ParallelConfigFactory::detect())
  ->setFinder($finder)
  ->setRules([
    '@PSR1' => true
  ])
  ->setHideProgress(true);
