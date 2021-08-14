-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-08-2021 a las 06:11:54
-- Versión del servidor: 10.4.20-MariaDB
-- Versión de PHP: 7.3.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `reporte`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `patrulla`
--

CREATE TABLE `patrulla` (
  `id_patrulla` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `placa_patrulla` varchar(10) NOT NULL,
  `id_basura` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `patrulla`
--

INSERT INTO `patrulla` (`id_patrulla`, `nombre`, `placa_patrulla`, `id_basura`) VALUES
(1, 'Sin patrulla', '000-000', '0'),
(3, 'Patrulla 1_1', 'JFJ-325', '1'),
(4, 'Patrulla 1_2', 'DKS-325', '1'),
(5, 'Patrulla 1_3', 'GGD-768', '1'),
(17, 'Patrulla 2_1', 'OUO-664', '2'),
(18, 'Patrulla 2_2', 'UYO-892', '2'),
(19, 'Patrulla 2_3', 'YUS-645', '2'),
(20, 'Patrulla 3_1', 'IOU-342', '3'),
(21, 'Patrulla 3_2', 'UTI-331', '3'),
(22, 'Patrulla 3_3', 'MAR-356', '3'),
(23, 'Patrulla 4_1', 'JHH-249', '4'),
(24, 'Patrulla 4_2', 'UOk-875', '4'),
(25, 'Patrulla 4_3', 'ITU-886', '4'),
(26, 'Patrulla 5_1', 'JUI-221', '5'),
(27, 'Patrulla 5_2', 'JNR-139', '5'),
(28, 'Patrulla 5_3', 'MRO-238', '5');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reporte`
--

CREATE TABLE `reporte` (
  `codigo_reporte` int(11) NOT NULL,
  `documento` varchar(20) NOT NULL,
  `poliza` varchar(20) CHARACTER SET utf8 NOT NULL,
  `barrio` varchar(255) NOT NULL,
  `direccion_rep` varchar(255) NOT NULL,
  `fecha_reporte` datetime NOT NULL,
  `descripcion` text NOT NULL,
  `estado` varchar(20) NOT NULL,
  `id_usuario` int(10) NOT NULL,
  `id_basura` varchar(10) NOT NULL,
  `id_patrulla` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `reporte`
--

INSERT INTO `reporte` (`codigo_reporte`, `documento`, `poliza`, `barrio`, `direccion_rep`, `fecha_reporte`, `descripcion`, `estado`, `id_usuario`, `id_basura`, `id_patrulla`) VALUES
(5, '1007451197', '525323', 'El Rubí', 'Cra 45 # 76 -89', '2021-08-12 21:12:43', 'Mucha basura en el anden.', 'Pendiente', 4, '5', 1),
(6, '1007451197', '525323', '20 de Julio', 'Cra 32 # 46 - 66', '2021-08-12 21:13:30', 'Hubo una rumba en frente de la tienda de \"Donde Paco\".', 'Pendiente', 4, '1', 1),
(7, '1014995593', '113411', '20 de Julio', 'Cra 46 # 47 - 78', '2021-08-12 21:22:39', 'Hubo una fiesta y dejaron toda la comida alli tirada.\r\n', 'Pendiente', 18, '4', 1),
(8, '1014995593', '113411', '20 de Julio', 'Calle 72 # 56 - 89', '2021-08-12 21:24:11', '', 'Pendiente', 18, '1', 1),
(9, '1938459842', '431413', 'Alfonso López', 'Cra 23 # 48 -98', '2021-08-12 21:26:55', '', 'Pendiente', 20, '1', 1),
(10, '1938459842', '431413', 'Altos de Riomar', 'Cra 89 # 45 -109', '2021-08-12 21:27:34', 'Enfrente del centro comercial viva.', 'Pendiente', 20, '1', 1),
(11, '1938459842', '431413', 'Rios de agua viva', 'Cra 35 # 46 -04', '2021-08-12 21:28:25', 'Hay muchas ramas en la va.', 'Pendiente', 20, '3', 1),
(12, '1938459842', '431413', 'Montes', 'Cra 39 # 45 - 08', '2021-08-12 21:29:17', 'Se cayo una casa en obra negra enfrente de la mia.', 'Pendiente', 20, '2', 1),
(13, '1192795459', '408329', 'El Rosario', 'Cra 54 # 65- 78', '2021-08-12 21:30:38', '', 'Pendiente', 15, '4', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_usuario`
--

CREATE TABLE `rol_usuario` (
  `id_rol` varchar(20) NOT NULL,
  `nombre_rol` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `rol_usuario`
--

INSERT INTO `rol_usuario` (`id_rol`, `nombre_rol`) VALUES
('1', 'usuario'),
('2', 'administrador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_basura`
--

CREATE TABLE `tipo_basura` (
  `id_basura` varchar(10) NOT NULL,
  `tipo_basura` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tipo_basura`
--

INSERT INTO `tipo_basura` (`id_basura`, `tipo_basura`) VALUES
('0', 'Sin especificar'),
('1', 'Basura'),
('2', 'Escombros'),
('3', 'Ramas y hojas'),
('4', 'Residuos organicos'),
('5', 'Vidrios y botellas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(10) NOT NULL,
  `documento` varchar(20) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `fecha_nac` date NOT NULL,
  `pais` varchar(30) NOT NULL,
  `ciudad` varchar(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `password` varchar(30) NOT NULL,
  `id_rol` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `documento`, `nombre`, `telefono`, `fecha_nac`, `pais`, `ciudad`, `email`, `password`, `id_rol`) VALUES
(4, '1007451197', 'Janer Cantillo', '3017242019', '2002-01-05', 'Colombia', 'Barranquilla', 'janer@gmail.com', 'Janer123', '2'),
(6, '1043125693', 'Jesús Fragoso', '3122056969', '2002-12-25', 'Colombia', 'Soledad', 'jesus@gmail.com', 'Jesus123', '2'),
(15, '1192795459', 'Mario Núñez', '3046449007', '2001-02-06', 'Colombia', 'Barranquilla', 'mario@gmail.com', 'Mario123', '2'),
(18, '1014995593', 'Rodrigo Lopez', '3103748595', '1995-05-19', 'Colombia', 'Soledad', 'rodrigo@gmail.com', 'Rodrigo123', '1'),
(19, '1013945839', 'Karen Rodríguez', '3122087666', '1999-12-11', 'Colombia', 'Santo Tomas', 'karen@gmail.com', 'Karen123', '1'),
(20, '1938459842', 'Mara Sofia Vergara', '3154806022', '2001-07-19', 'Colombia', 'Soledad', 'maritaver45@gmail.com', 'Marasofia12', '1');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `patrulla`
--
ALTER TABLE `patrulla`
  ADD PRIMARY KEY (`id_patrulla`),
  ADD KEY `id_basura` (`id_basura`);

--
-- Indices de la tabla `reporte`
--
ALTER TABLE `reporte`
  ADD PRIMARY KEY (`codigo_reporte`),
  ADD KEY `documento_usuario` (`id_usuario`),
  ADD KEY `id_basura` (`id_basura`),
  ADD KEY `id_patrulla` (`id_patrulla`);

--
-- Indices de la tabla `rol_usuario`
--
ALTER TABLE `rol_usuario`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `tipo_basura`
--
ALTER TABLE `tipo_basura`
  ADD PRIMARY KEY (`id_basura`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `patrulla`
--
ALTER TABLE `patrulla`
  MODIFY `id_patrulla` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de la tabla `reporte`
--
ALTER TABLE `reporte`
  MODIFY `codigo_reporte` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `patrulla`
--
ALTER TABLE `patrulla`
  ADD CONSTRAINT `patrulla_ibfk_1` FOREIGN KEY (`id_basura`) REFERENCES `tipo_basura` (`id_basura`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `reporte`
--
ALTER TABLE `reporte`
  ADD CONSTRAINT `reporte_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `reporte_ibfk_4` FOREIGN KEY (`id_basura`) REFERENCES `tipo_basura` (`id_basura`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `reporte_ibfk_5` FOREIGN KEY (`id_patrulla`) REFERENCES `patrulla` (`id_patrulla`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `rol_usuario` (`id_rol`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
