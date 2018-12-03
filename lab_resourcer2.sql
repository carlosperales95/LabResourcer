-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-12-2018 a las 19:43:45
-- Versión del servidor: 10.1.13-MariaDB
-- Versión de PHP: 5.6.23

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `lab_resourcer`
--
CREATE DATABASE IF NOT EXISTS `lab_resourcer` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `lab_resourcer`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `binding`
--

CREATE TABLE `binding` (
  `primary_antibody_id` int(11) NOT NULL,
  `staining_id` int(11) NOT NULL,
  `secondary_antibody_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELACIONES PARA LA TABLA `binding`:
--   `primary_antibody_id`
--       `primary_antibody` -> `primary_antibody_id`
--   `secondary_antibody_id`
--       `secondary_antibody` -> `secondary_antibody_id`
--   `staining_id`
--       `staining` -> `staining_id`
--

--
-- Volcado de datos para la tabla `binding`
--

INSERT INTO `binding` (`primary_antibody_id`, `staining_id`, `secondary_antibody_id`) VALUES
(1, 10, 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `chemical`
--

CREATE TABLE `chemical` (
  `chemical_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELACIONES PARA LA TABLA `chemical`:
--

--
-- Volcado de datos para la tabla `chemical`
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
(12, 'Stay-Yellow');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `color`
--

CREATE TABLE `color` (
  `color_id` int(11) NOT NULL,
  `staining_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELACIONES PARA LA TABLA `color`:
--   `staining_id`
--       `staining` -> `staining_id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `experiment`
--

CREATE TABLE `experiment` (
  `experiment_id` int(11) NOT NULL,
  `researcher_id` int(11) NOT NULL,
  `tissue_slices` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELACIONES PARA LA TABLA `experiment`:
--   `researcher_id`
--       `researcher` -> `researcher_id`
--

--
-- Volcado de datos para la tabla `experiment`
--

INSERT INTO `experiment` (`experiment_id`, `researcher_id`, `tissue_slices`) VALUES
(1, 1, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `experiment_chemical`
--

CREATE TABLE `experiment_chemical` (
  `experiment_id` int(11) NOT NULL,
  `chemical_id` int(11) NOT NULL,
  `amount` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELACIONES PARA LA TABLA `experiment_chemical`:
--   `chemical_id`
--       `chemical` -> `chemical_id`
--   `experiment_id`
--       `experiment` -> `experiment_id`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventory`
--

CREATE TABLE `inventory` (
  `inventory_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELACIONES PARA LA TABLA `inventory`:
--

--
-- Volcado de datos para la tabla `inventory`
--

INSERT INTO `inventory` (`inventory_id`) VALUES
(1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventory_chemical`
--

CREATE TABLE `inventory_chemical` (
  `inventory_id` int(11) NOT NULL,
  `chemical_id` int(11) NOT NULL,
  `amount` float NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELACIONES PARA LA TABLA `inventory_chemical`:
--   `chemical_id`
--       `chemical` -> `chemical_id`
--   `inventory_id`
--       `inventory` -> `inventory_id`
--

--
-- Volcado de datos para la tabla `inventory_chemical`
--

INSERT INTO `inventory_chemical` (`inventory_id`, `chemical_id`, `amount`) VALUES
(1, 1, 0.2),
(1, 2, 200),
(1, 3, 300),
(1, 4, 450),
(1, 5, 100),
(1, 6, 0),
(1, 7, 0.34),
(1, 8, 0.1),
(1, 9, 0.12),
(1, 10, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `primary_antibody`
--

CREATE TABLE `primary_antibody` (
  `primary_antibody_id` int(11) NOT NULL,
  `animal` varchar(30) NOT NULL,
  `dilution` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELACIONES PARA LA TABLA `primary_antibody`:
--   `primary_antibody_id`
--       `chemical` -> `chemical_id`
--

--
-- Volcado de datos para la tabla `primary_antibody`
--

INSERT INTO `primary_antibody` (`primary_antibody_id`, `animal`, `dilution`) VALUES
(1, 'Mouse', 0.002);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `protocol`
--

CREATE TABLE `protocol` (
  `protocol_id` int(11) NOT NULL,
  `chemical_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELACIONES PARA LA TABLA `protocol`:
--   `chemical_id`
--       `chemical` -> `chemical_id`
--

--
-- Volcado de datos para la tabla `protocol`
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
-- Estructura de tabla para la tabla `researcher`
--

CREATE TABLE `researcher` (
  `researcher_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELACIONES PARA LA TABLA `researcher`:
--

--
-- Volcado de datos para la tabla `researcher`
--

INSERT INTO `researcher` (`researcher_id`, `name`) VALUES
(1, 'Irene Frigerio');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `secondary_antibody`
--

CREATE TABLE `secondary_antibody` (
  `secondary_antibody_id` int(11) NOT NULL,
  `animal` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELACIONES PARA LA TABLA `secondary_antibody`:
--   `secondary_antibody_id`
--       `chemical` -> `chemical_id`
--

--
-- Volcado de datos para la tabla `secondary_antibody`
--

INSERT INTO `secondary_antibody` (`secondary_antibody_id`, `animal`) VALUES
(9, 'Mouse');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `staining`
--

CREATE TABLE `staining` (
  `staining_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELACIONES PARA LA TABLA `staining`:
--   `staining_id`
--       `chemical` -> `chemical_id`
--

--
-- Volcado de datos para la tabla `staining`
--

INSERT INTO `staining` (`staining_id`) VALUES
(10),
(11),
(12);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `binding`
--
ALTER TABLE `binding`
  ADD PRIMARY KEY (`primary_antibody_id`,`staining_id`),
  ADD KEY `binding_id` (`primary_antibody_id`,`staining_id`,`secondary_antibody_id`);

--
-- Indices de la tabla `chemical`
--
ALTER TABLE `chemical`
  ADD PRIMARY KEY (`chemical_id`);

--
-- Indices de la tabla `color`
--
ALTER TABLE `color`
  ADD PRIMARY KEY (`color_id`),
  ADD KEY `staining_id` (`staining_id`);

--
-- Indices de la tabla `experiment`
--
ALTER TABLE `experiment`
  ADD PRIMARY KEY (`experiment_id`),
  ADD KEY `researcher_id` (`researcher_id`);

--
-- Indices de la tabla `experiment_chemical`
--
ALTER TABLE `experiment_chemical`
  ADD PRIMARY KEY (`experiment_id`,`chemical_id`),
  ADD KEY `experiment_chemical_id` (`experiment_id`,`chemical_id`);

--
-- Indices de la tabla `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`inventory_id`);

--
-- Indices de la tabla `inventory_chemical`
--
ALTER TABLE `inventory_chemical`
  ADD PRIMARY KEY (`inventory_id`,`chemical_id`),
  ADD KEY `inventory_chemical_id` (`inventory_id`,`chemical_id`);

--
-- Indices de la tabla `primary_antibody`
--
ALTER TABLE `primary_antibody`
  ADD PRIMARY KEY (`primary_antibody_id`),
  ADD KEY `chemical_id` (`primary_antibody_id`);

--
-- Indices de la tabla `protocol`
--
ALTER TABLE `protocol`
  ADD PRIMARY KEY (`protocol_id`,`chemical_id`),
  ADD KEY `chemical_id` (`chemical_id`);

--
-- Indices de la tabla `researcher`
--
ALTER TABLE `researcher`
  ADD PRIMARY KEY (`researcher_id`);

--
-- Indices de la tabla `secondary_antibody`
--
ALTER TABLE `secondary_antibody`
  ADD PRIMARY KEY (`secondary_antibody_id`),
  ADD KEY `chemical_id` (`secondary_antibody_id`);

--
-- Indices de la tabla `staining`
--
ALTER TABLE `staining`
  ADD PRIMARY KEY (`staining_id`),
  ADD KEY `chemical_id` (`staining_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `chemical`
--
ALTER TABLE `chemical`
  MODIFY `chemical_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
--
-- AUTO_INCREMENT de la tabla `experiment`
--
ALTER TABLE `experiment`
  MODIFY `experiment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT de la tabla `inventory`
--
ALTER TABLE `inventory`
  MODIFY `inventory_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT de la tabla `researcher`
--
ALTER TABLE `researcher`
  MODIFY `researcher_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;SET FOREIGN_KEY_CHECKS=1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
