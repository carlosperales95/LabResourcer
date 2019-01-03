-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 03, 2019 at 07:09 PM
-- Server version: 5.7.24-0ubuntu0.18.04.1
-- PHP Version: 7.2.10-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lab_resourcer`
--
CREATE DATABASE IF NOT EXISTS `lab_resourcer` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `lab_resourcer`;

-- --------------------------------------------------------

--
-- Table structure for table `binding`
--

CREATE TABLE `binding` (
  `primary_antibody_id` int(11) NOT NULL,
  `staining_id` int(11) NOT NULL,
  `secondary_antibody_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `binding`
--

INSERT INTO `binding` (`primary_antibody_id`, `staining_id`, `secondary_antibody_id`) VALUES
(1, 10, 9),
(1, 11, 22),
(1, 12, 9),
(21, 10, 9),
(21, 11, 22),
(21, 12, 9),
(23, 10, 9),
(23, 11, 22),
(23, 12, 9),
(24, 10, 9),
(24, 11, 22),
(24, 12, 9),
(25, 10, 9),
(25, 11, 22),
(25, 12, 9),
(26, 10, 9),
(26, 11, 22),
(26, 12, 9),
(27, 10, 9),
(27, 11, 22),
(27, 12, 9);

-- --------------------------------------------------------

--
-- Table structure for table `chemical`
--

CREATE TABLE `chemical` (
  `chemical_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `chemical`
--

INSERT INTO `chemical` (`chemical_id`, `name`) VALUES
(1, 'Anti-PLP'),
(2, 'Aceton'),
(3, 'Tris/EDTA pH9'),
(4, '35%H2O2'),
(5, 'TBS'),
(6, 'Triton'),
(7, 'NDS'),
(8, 'Mowiol+DABCO'),
(9, 'Envision'),
(10, 'Vector-SG'),
(11, 'Liquid Permanent Red'),
(12, 'Stay-Yellow'),
(21, 'Alpha-peptdyl'),
(22, 'Impress'),
(23, 'Anti-SMI'),
(24, 'NF155'),
(25, 'Citrulline'),
(26, 'Anti-MBP'),
(27, 'Anti-MAG');

-- --------------------------------------------------------

--
-- Table structure for table `color`
--

CREATE TABLE `color` (
  `color_id` int(11) NOT NULL,
  `staining_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `experiment`
--

CREATE TABLE `experiment` (
  `experiment_id` int(11) NOT NULL,
  `researcher_id` int(11) NOT NULL,
  `tissue_slices` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `experiment`
--

INSERT INTO `experiment` (`experiment_id`, `researcher_id`, `tissue_slices`) VALUES
(1, 1, 7),
(2, 1, 7),
(3, 1, 1),
(4, 1, 7),
(5, 4, 5),
(6, 4, 3),
(7, 4, 10);

-- --------------------------------------------------------

--
-- Table structure for table `experiment_chemical`
--

CREATE TABLE `experiment_chemical` (
  `experiment_id` int(11) NOT NULL,
  `chemical_id` int(11) NOT NULL,
  `amount` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `experiment_chemical`
--

INSERT INTO `experiment_chemical` (`experiment_id`, `chemical_id`, `amount`) VALUES
(7, 2, 120),
(7, 3, 240),
(7, 4, 20.56),
(7, 6, 0.21),
(7, 7, 0.252),
(7, 9, 1),
(7, 10, 2),
(7, 11, 2),
(7, 21, 0.028),
(7, 22, 1),
(7, 27, 0.0042);

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `inventory_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`inventory_id`) VALUES
(1);

-- --------------------------------------------------------

--
-- Table structure for table `inventory_chemical`
--

CREATE TABLE `inventory_chemical` (
  `inventory_id` int(11) NOT NULL,
  `chemical_id` int(11) NOT NULL,
  `amount` float NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `inventory_chemical`
--

INSERT INTO `inventory_chemical` (`inventory_id`, `chemical_id`, `amount`) VALUES
(1, 1, 0.2),
(1, 2, 200),
(1, 3, 300),
(1, 4, 450),
(1, 5, 100),
(1, 6, 10),
(1, 7, 0.34),
(1, 8, 0.1),
(1, 9, 10),
(1, 10, 10),
(1, 11, 20),
(1, 12, 50),
(1, 21, 5),
(1, 22, 10),
(1, 23, 7),
(1, 24, 0),
(1, 25, 150),
(1, 26, 200),
(1, 27, 70);

-- --------------------------------------------------------

--
-- Table structure for table `primary_antibody`
--

CREATE TABLE `primary_antibody` (
  `primary_antibody_id` int(11) NOT NULL,
  `animal` varchar(30) NOT NULL,
  `dilution` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `primary_antibody`
--

INSERT INTO `primary_antibody` (`primary_antibody_id`, `animal`, `dilution`) VALUES
(1, 'Mouse', 500),
(21, 'Mouse', 150),
(23, 'Mouse', 1000),
(24, 'Rabbit', 50),
(25, 'Mouse', 150),
(26, 'Mouse', 1000),
(27, 'Rabbit', 1000);

-- --------------------------------------------------------

--
-- Table structure for table `protocol`
--

CREATE TABLE `protocol` (
  `protocol_id` int(11) NOT NULL,
  `chemical_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `protocol`
--

INSERT INTO `protocol` (`protocol_id`, `chemical_id`) VALUES
(8, 2),
(8, 3),
(8, 4),
(8, 5),
(8, 6),
(8, 7),
(8, 8);

-- --------------------------------------------------------

--
-- Table structure for table `researcher`
--

CREATE TABLE `researcher` (
  `researcher_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `researcher`
--

INSERT INTO `researcher` (`researcher_id`, `name`) VALUES
(1, 'Irene Frigerio'),
(2, 'Diana Ton'),
(3, 'Elbert Pauwel'),
(4, 'Renee Melle '),
(5, 'Maikel Boele '),
(6, 'Marco Aris ');

-- --------------------------------------------------------

--
-- Table structure for table `secondary_antibody`
--

CREATE TABLE `secondary_antibody` (
  `secondary_antibody_id` int(11) NOT NULL,
  `animal` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `secondary_antibody`
--

INSERT INTO `secondary_antibody` (`secondary_antibody_id`, `animal`) VALUES
(9, 'Mouse'),
(22, 'Mouse');

-- --------------------------------------------------------

--
-- Table structure for table `staining`
--

CREATE TABLE `staining` (
  `staining_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `staining`
--

INSERT INTO `staining` (`staining_id`) VALUES
(10),
(11),
(12);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `binding`
--
ALTER TABLE `binding`
  ADD PRIMARY KEY (`primary_antibody_id`,`staining_id`),
  ADD KEY `binding_id` (`primary_antibody_id`,`staining_id`,`secondary_antibody_id`);

--
-- Indexes for table `chemical`
--
ALTER TABLE `chemical`
  ADD PRIMARY KEY (`chemical_id`);

--
-- Indexes for table `color`
--
ALTER TABLE `color`
  ADD PRIMARY KEY (`color_id`),
  ADD KEY `staining_id` (`staining_id`);

--
-- Indexes for table `experiment`
--
ALTER TABLE `experiment`
  ADD PRIMARY KEY (`experiment_id`),
  ADD KEY `researcher_id` (`researcher_id`);

--
-- Indexes for table `experiment_chemical`
--
ALTER TABLE `experiment_chemical`
  ADD PRIMARY KEY (`experiment_id`,`chemical_id`),
  ADD KEY `experiment_chemical_id` (`experiment_id`,`chemical_id`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`inventory_id`);

--
-- Indexes for table `inventory_chemical`
--
ALTER TABLE `inventory_chemical`
  ADD PRIMARY KEY (`inventory_id`,`chemical_id`),
  ADD KEY `inventory_chemical_id` (`inventory_id`,`chemical_id`);

--
-- Indexes for table `primary_antibody`
--
ALTER TABLE `primary_antibody`
  ADD PRIMARY KEY (`primary_antibody_id`),
  ADD KEY `chemical_id` (`primary_antibody_id`);

--
-- Indexes for table `protocol`
--
ALTER TABLE `protocol`
  ADD PRIMARY KEY (`protocol_id`,`chemical_id`),
  ADD KEY `chemical_id` (`chemical_id`);

--
-- Indexes for table `researcher`
--
ALTER TABLE `researcher`
  ADD PRIMARY KEY (`researcher_id`);

--
-- Indexes for table `secondary_antibody`
--
ALTER TABLE `secondary_antibody`
  ADD PRIMARY KEY (`secondary_antibody_id`),
  ADD KEY `chemical_id` (`secondary_antibody_id`);

--
-- Indexes for table `staining`
--
ALTER TABLE `staining`
  ADD PRIMARY KEY (`staining_id`),
  ADD KEY `chemical_id` (`staining_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `chemical`
--
ALTER TABLE `chemical`
  MODIFY `chemical_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
--
-- AUTO_INCREMENT for table `experiment`
--
ALTER TABLE `experiment`
  MODIFY `experiment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `inventory_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `researcher`
--
ALTER TABLE `researcher`
  MODIFY `researcher_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
