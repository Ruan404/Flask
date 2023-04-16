-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le :  Dim 16 avr. 2023 à 19:23
-- Version du serveur :  5.7.26
-- Version de PHP :  7.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `flask`
--

-- --------------------------------------------------------

--
-- Structure de la table `campus`
--

DROP TABLE IF EXISTS `campus`;
CREATE TABLE IF NOT EXISTS `campus` (
  `idCampus` int(11) NOT NULL AUTO_INCREMENT,
  `campusName` varchar(45) NOT NULL,
  PRIMARY KEY (`idCampus`),
  UNIQUE KEY `campusName_UNIQUE` (`campusName`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `campus`
--

INSERT INTO `campus` (`idCampus`, `campusName`) VALUES
(12, 'Bordeaux');

-- --------------------------------------------------------

--
-- Structure de la table `mobilitywish`
--

DROP TABLE IF EXISTS `mobilitywish`;
CREATE TABLE IF NOT EXISTS `mobilitywish` (
  `idMobilityWish` int(11) NOT NULL AUTO_INCREMENT,
  `studentMail` varchar(45) NOT NULL,
  `Campus_idCampus` int(11) NOT NULL,
  PRIMARY KEY (`idMobilityWish`,`Campus_idCampus`),
  KEY `fk_MobilityWish_Campus_idx` (`Campus_idCampus`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(20) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` varchar(5) NOT NULL DEFAULT 'user',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`user_id`, `email`, `password`, `role`) VALUES
(2, 'admin@gmail.com', '87654321', 'admin'),
(8, 'jean@gmail.com', '12345678', 'user');

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `mobilitywish`
--
ALTER TABLE `mobilitywish`
  ADD CONSTRAINT `fk_MobilityWish_Campus` FOREIGN KEY (`Campus_idCampus`) REFERENCES `campus` (`idCampus`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
