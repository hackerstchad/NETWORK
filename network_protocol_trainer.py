#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Network Protocol Trainer
An advanced Tkinter educational game to learn network protocols and acronyms.
Supports learning mode, multiple quiz modes, scoring, streaks, and search.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
from collections import defaultdict

# -----------------------------------------------------------------------------
# Protocol Database
# -----------------------------------------------------------------------------

PROTOCOLS = {
    # Couche Réseau
    "IP": {
        "name": "Internet Protocol",
        "category": "Couche Réseau",
        "description": "Protocole fondamental d'adressage et de routage des paquets sur Internet.",
        "details": "IPv4 utilise des adresses 32 bits ; IPv6 utilise des adresses 128 bits.",
        "ports": "N/A (couche 3)",
        "layer": 3,
        "rfc": "RFC 791 (IPv4), RFC 8200 (IPv6)"
    },
    "IPv4": {
        "name": "Internet Protocol version 4",
        "category": "Couche Réseau",
        "description": "Quatrième version du protocole IP avec adresses 32 bits.",
        "details": "Notation décimale pointée : 192.0.2.1. Environ 4,3 milliards d'adresses.",
        "ports": "N/A (couche 3)",
        "layer": 3,
        "rfc": "RFC 791"
    },
    "IPv6": {
        "name": "Internet Protocol version 6",
        "category": "Couche Réseau",
        "description": "Successeur d'IPv4 avec adresses 128 bits.",
        "details": "Notation hexadécimale groupée : 2001:0db8::1. Résout l'épuisement d'IPv4.",
        "ports": "N/A (couche 3)",
        "layer": 3,
        "rfc": "RFC 8200"
    },
    "ICMP": {
        "name": "Internet Control Message Protocol",
        "category": "Couche Réseau",
        "description": "Utilisé pour envoyer des messages de contrôle et d'erreur.",
        "details": "ping utilise les requêtes/réponses ICMP Echo (type 8 / 0).",
        "ports": "N/A (protocole 1 sur IP)",
        "layer": 3,
        "rfc": "RFC 792"
    },
    "IGMP": {
        "name": "Internet Group Management Protocol",
        "category": "Couche Réseau",
        "description": "Gère l'appartenance des hôtes à des groupes multicast.",
        "details": "Utilisé par les routeurs pour connaître les groupes actifs sur un segment.",
        "ports": "N/A (protocole 2 sur IP)",
        "layer": 3,
        "rfc": "RFC 3376"
    },
    "ARP": {
        "name": "Address Resolution Protocol",
        "category": "Couche Réseau",
        "description": "Associe une adresse IP à une adresse MAC sur un réseau local.",
        "details": "Envoie une requête broadcast : 'Qui a cette IP ?'",
        "ports": "N/A",
        "layer": 2.5,
        "rfc": "RFC 826"
    },
    "RARP": {
        "name": "Reverse Address Resolution Protocol",
        "category": "Couche Réseau",
        "description": "Permet à une station de découvrir son adresse IP à partir de son MAC.",
        "details": "Aujourd'hui remplacé principalement par DHCP.",
        "ports": "N/A",
        "layer": 2.5,
        "rfc": "RFC 903"
    },
    "NDP": {
        "name": "Neighbor Discovery Protocol",
        "category": "Couche Réseau",
        "description": "Fonction IPv6 équivalente à ARP, découvre les voisins et les routeurs.",
        "details": "Utilise des messages ICMPv6 (types 135/136 pour voisins).",
        "ports": "N/A",
        "layer": 3,
        "rfc": "RFC 4861"
    },
    "MPLS": {
        "name": "Multiprotocol Label Switching",
        "category": "Couche Réseau",
        "description": "Commutation de paquets par étiquettes pour des chemins prédéfinis.",
        "details": "Souvent utilisé par les FAI pour la QoS et les VPN.",
        "ports": "N/A",
        "layer": 2.5,
        "rfc": "RFC 3031"
    },

    # Couche Transport
    "TCP": {
        "name": "Transmission Control Protocol",
        "category": "Couche Transport",
        "description": "Protocole orienté connexion, fiable, avec contrôle de flux.",
        "details": "Handshake en 3 étapes, acquittements, retransmission.",
        "ports": "Variable (ex: 80, 443, 22)",
        "layer": 4,
        "rfc": "RFC 793"
    },
    "UDP": {
        "name": "User Datagram Protocol",
        "category": "Couche Transport",
        "description": "Protocole sans connexion, rapide, non fiable.",
        "details": "Idéal pour streaming, jeux, DNS où la latence prime.",
        "ports": "Variable (ex: 53, 123, 5060)",
        "layer": 4,
        "rfc": "RFC 768"
    },
    "SCTP": {
        "name": "Stream Control Transmission Protocol",
        "category": "Couche Transport",
        "description": "Transport fiable avec multi-homing et multi-streaming.",
        "details": "Utilisé en téléphonie sur IP (SIGTRAN).",
        "ports": "Variable",
        "layer": 4,
        "rfc": "RFC 4960"
    },
    "DCCP": {
        "name": "Datagram Congestion Control Protocol",
        "category": "Couche Transport",
        "description": "Protocole orienté datagramme avec contrôle de congestion.",
        "details": "Combine aspects d'UDP et TCP.",
        "ports": "Variable",
        "layer": 4,
        "rfc": "RFC 4340"
    },
    "QUIC": {
        "name": "Quick UDP Internet Connections",
        "category": "Couche Transport",
        "description": "Transport sécurisé sur UDP avec faible latence.",
        "details": "HTTP/3 repose sur QUIC.",
        "ports": "UDP 443 (typiquement)",
        "layer": 4,
        "rfc": "RFC 9000"
    },

    # Routage
    "BGP": {
        "name": "Border Gateway Protocol",
        "category": "Routage",
        "description": "Protocole de routage externe entre systèmes autonomes.",
        "details": "Routage de l'Internet mondial. Versions : BGP-4, BGP avec MP-BGP.",
        "ports": "TCP 179",
        "layer": 7,
        "rfc": "RFC 4271"
    },
    "OSPF": {
        "name": "Open Shortest Path First",
        "category": "Routage",
        "description": "Protocole de routage interne à état de liens.",
        "details": "Utilise l'algorithme de Dijkstra. Supporte IPv4 et IPv6 (OSPFv3).",
        "ports": "IP 89",
        "layer": 3,
        "rfc": "RFC 2328"
    },
    "RIP": {
        "name": "Routing Information Protocol",
        "category": "Routage",
        "description": "Protocole de routage interne à vecteur de distance.",
        "details": "Limite de 15 sauts. Versions : RIP v1, v2, RIPng pour IPv6.",
        "ports": "UDP 520",
        "layer": 3,
        "rfc": "RFC 2453"
    },
    "IS-IS": {
        "name": "Intermediate System to Intermediate System",
        "category": "Routage",
        "description": "Protocole de routage à état de liens utilisé par les FAI.",
        "details": "Fonctionne directement sur la couche liaison.",
        "ports": "N/A",
        "layer": 2,
        "rfc": "ISO/IEC 10589"
    },
    "EIGRP": {
        "name": "Enhanced Interior Gateway Routing Protocol",
        "category": "Routage",
        "description": "Protocole propriétaire Cisco hybride avancé.",
        "details": "Utilise DUAL pour calculer les chemins sans boucles.",
        "ports": "IP 88",
        "layer": 3,
        "rfc": "RFC 7868"
    },

    # Attribution d'adresses
    "DHCP": {
        "name": "Dynamic Host Configuration Protocol",
        "category": "Attribution d'adresses",
        "description": "Attribue automatiquement IP, masque, passerelle et DNS.",
        "details": "Processus DORA : Discover, Offer, Request, Acknowledge.",
        "ports": "UDP 67 (serveur), UDP 68 (client)",
        "layer": 7,
        "rfc": "RFC 2131"
    },
    "BOOTP": {
        "name": "Bootstrap Protocol",
        "category": "Attribution d'adresses",
        "description": "Prédécesseur de DHCP sans attribution dynamique.",
        "details": "Nécessite une table statique MAC/IP.",
        "ports": "UDP 67/68",
        "layer": 7,
        "rfc": "RFC 951"
    },

    # Résolution de noms
    "DNS": {
        "name": "Domain Name System",
        "category": "Résolution de noms",
        "description": "Traduit les noms de domaine en adresses IP.",
        "details": "Hiérarchique et distribué. Types d'enregistrements : A, AAAA, MX, TXT, CNAME...",
        "ports": "UDP 53 (requêtes), TCP 53 (transferts de zone)",
        "layer": 7,
        "rfc": "RFC 1035"
    },
    "mDNS": {
        "name": "Multicast DNS",
        "category": "Résolution de noms",
        "description": "Résolution de noms sans serveur DNS via multicast.",
        "details": "Utilisé par Bonjour/mDNSResponder en local.",
        "ports": "UDP 5353",
        "layer": 7,
        "rfc": "RFC 6762"
    },
    "LLMNR": {
        "name": "Link-Local Multicast Name Resolution",
        "category": "Résolution de noms",
        "description": "Résolution de noms locale sur un segment réseau.",
        "details": "Principalement utilisé dans les réseaux Windows.",
        "ports": "UDP 5355",
        "layer": 7,
        "rfc": "RFC 4795"
    },

    # Web
    "HTTP": {
        "name": "HyperText Transfer Protocol",
        "category": "Web",
        "description": "Protocole de transfert web en clair.",
        "details": "Méthodes : GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS.",
        "ports": "TCP 80",
        "layer": 7,
        "rfc": "RFC 9112"
    },
    "HTTPS": {
        "name": "HyperText Transfer Protocol Secure",
        "category": "Web",
        "description": "HTTP sécurisé par TLS/SSL.",
        "details": "Par défaut TLS 1.2/1.3. Certificats X.509.",
        "ports": "TCP 443",
        "layer": 7,
        "rfc": "RFC 9110"
    },
    "HTTP/2": {
        "name": "HTTP version 2",
        "category": "Web",
        "description": "Multiplexage des flux sur une seule connexion TCP.",
        "details": "Compression HPACK des en-têtes.",
        "ports": "TCP 443 (typiquement)",
        "layer": 7,
        "rfc": "RFC 7540"
    },
    "HTTP/3": {
        "name": "HTTP version 3",
        "category": "Web",
        "description": "HTTP basé sur QUIC/UDP.",
        "details": "Réduit la latence et résout le head-of-line blocking.",
        "ports": "UDP 443 (typiquement)",
        "layer": 7,
        "rfc": "RFC 9114"
    },
    "WebSocket": {
        "name": "WebSocket Protocol",
        "category": "Web",
        "description": "Communication bidirectionnelle persistante sur TCP.",
        "details": "Handshakes HTTP puis connexion full-duplex.",
        "ports": "TCP 80/443",
        "layer": 7,
        "rfc": "RFC 6455"
    },

    # Transfert de fichiers
    "FTP": {
        "name": "File Transfer Protocol",
        "category": "Transfert de fichiers",
        "description": "Transfert de fichiers en clair avec canaux de contrôle et de données.",
        "details": "Actif/passif. Ports 21 (contrôle) et 20 (données).",
        "ports": "TCP 21 (contrôle), TCP 20 (données)",
        "layer": 7,
        "rfc": "RFC 959"
    },
    "FTPS": {
        "name": "FTP Secure",
        "category": "Transfert de fichiers",
        "description": "FTP sécurisé par TLS/SSL.",
        "details": "FTPS explicite vs implicite.",
        "ports": "TCP 21/990",
        "layer": 7,
        "rfc": "RFC 4217, RFC 959"
    },
    "SFTP": {
        "name": "SSH File Transfer Protocol",
        "category": "Transfert de fichiers",
        "description": "Transfert de fichiers sur un tunnel SSH.",
        "details": "Sous-système SSH. Port 22.",
        "ports": "TCP 22",
        "layer": 7,
        "rfc": "RFC 4251 (SSH)"
    },
    "TFTP": {
        "name": "Trivial File Transfer Protocol",
        "category": "Transfert de fichiers",
        "description": "Version simplifiée et non sécurisée de FTP.",
        "details": "Utilisé pour boot réseau (PXE) et transferts simples.",
        "ports": "UDP 69",
        "layer": 7,
        "rfc": "RFC 1350"
    },
    "SCP": {
        "name": "Secure Copy Protocol",
        "category": "Transfert de fichiers",
        "description": "Copie de fichiers sécurisée via SSH.",
        "details": "Commande 'scp' sous Unix/Linux.",
        "ports": "TCP 22",
        "layer": 7,
        "rfc": "Protocole SSH"
    },
    "Rsync": {
        "name": "Remote Sync",
        "category": "Transfert de fichiers",
        "description": "Synchronisation efficace de fichiers avec delta-transfer.",
        "details": "Ne transfère que les différences. Peut utiliser SSH.",
        "ports": "TCP 873 (rsync natif), TCP 22 (sur SSH)",
        "layer": 7,
        "rfc": "N/A"
    },

    # Courrier électronique
    "SMTP": {
        "name": "Simple Mail Transfer Protocol",
        "category": "Courrier électronique",
        "description": "Envoi de courriels entre serveurs et clients.",
        "details": "Extensions : ESMTP, STARTTLS, AUTH.",
        "ports": "TCP 25, 587 (submission), 465 (SMTPS)",
        "layer": 7,
        "rfc": "RFC 5321"
    },
    "POP3": {
        "name": "Post Office Protocol version 3",
        "category": "Courrier électronique",
        "description": "Récupération de courriels avec téléchargement local.",
        "details": "Messages généralement supprimés du serveur.",
        "ports": "TCP 110, 995 (POP3S)",
        "layer": 7,
        "rfc": "RFC 1939"
    },
    "IMAP": {
        "name": "Internet Message Access Protocol",
        "category": "Courrier électronique",
        "description": "Accès et synchronisation des courriels sur le serveur.",
        "details": "Supporte les dossiers et la synchronisation multi-appareils.",
        "ports": "TCP 143, 993 (IMAPS)",
        "layer": 7,
        "rfc": "RFC 3501"
    },

    # Accès distant
    "SSH": {
        "name": "Secure Shell",
        "category": "Accès distant",
        "description": "Accès sécurisé à distance et exécution de commandes.",
        "details": "Chiffre la session, supporte SCP/SFTP et le tunneling.",
        "ports": "TCP 22",
        "layer": 7,
        "rfc": "RFC 4251"
    },
    "Telnet": {
        "name": "Teletype Network",
        "category": "Accès distant",
        "description": "Accès distant en clair, aujourd'hui obsolète.",
        "details": "Remplacé par SSH pour des raisons de sécurité.",
        "ports": "TCP 23",
        "layer": 7,
        "rfc": "RFC 854"
    },
    "RDP": {
        "name": "Remote Desktop Protocol",
        "category": "Accès distant",
        "description": "Protocole Microsoft pour le bureau à distance.",
        "details": "Basé sur TPKT, inclut chiffrement et partage de presse-papiers.",
        "ports": "TCP/UDP 3389",
        "layer": 7,
        "rfc": "Propriétaire Microsoft"
    },
    "VNC": {
        "name": "Virtual Network Computing",
        "category": "Accès distant",
        "description": "Partage d'écran à distance multiplateforme.",
        "details": "Utilise le framebuffer RFB.",
        "ports": "TCP 5900+n",
        "layer": 7,
        "rfc": "RFB 3.8"
    },

    # Sécurité
    "TLS": {
        "name": "Transport Layer Security",
        "category": "Sécurité",
        "description": "Cryptographie pour sécuriser les communications.",
        "details": "Versions actuelles : TLS 1.2 et TLS 1.3.",
        "ports": "TCP 443 (typiquement)",
        "layer": 5,
        "rfc": "RFC 8446"
    },
    "SSL": {
        "name": "Secure Sockets Layer",
        "category": "Sécurité",
        "description": "Ancêtre de TLS, aujourd'hui obsolète.",
        "details": "SSL 2.0 et 3.0 désactivés pour vulnérabilités (POODLE).",
        "ports": "TCP 443 (historiquement)",
        "layer": 5,
        "rfc": "Historique"
    },
    "IPsec": {
        "name": "Internet Protocol Security",
        "category": "Sécurité",
        "description": "Sécurisation des paquets IP (VPN, confidentialité, intégrité).",
        "details": "Modes transport et tunnel. Protocoles AH et ESP.",
        "ports": "ESP 50, AH 51, UDP 500 (IKE)",
        "layer": 3,
        "rfc": "RFC 4301"
    },
    "Kerberos": {
        "name": "Kerberos",
        "category": "Sécurité",
        "description": "Authentification centralisée par tickets.",
        "details": "Utilisé dans Active Directory. Basé sur la cryptographie symétrique.",
        "ports": "TCP/UDP 88",
        "layer": 7,
        "rfc": "RFC 4120"
    },
    "OAuth 2.0": {
        "name": "Open Authorization 2.0",
        "category": "Sécurité",
        "description": "Cadre d'autorisation déléguée pour applications tierces.",
        "details": "Flux : Authorization Code, Client Credentials, Device Code...",
        "ports": "HTTPS",
        "layer": 7,
        "rfc": "RFC 6749"
    },
    "OpenID Connect": {
        "name": "OpenID Connect",
        "category": "Sécurité",
        "description": "Couche d'identité au-dessus d'OAuth 2.0.",
        "details": "Fournit un token JWT contenant l'identité de l'utilisateur.",
        "ports": "HTTPS",
        "layer": 7,
        "rfc": "OpenID Connect Core 1.0"
    },

    # Synchronisation
    "NTP": {
        "name": "Network Time Protocol",
        "category": "Synchronisation",
        "description": "Synchronisation de l'heure entre systèmes.",
        "details": "Précision millisecondes. Utilise des strates.",
        "ports": "UDP 123",
        "layer": 7,
        "rfc": "RFC 5905"
    },
    "PTP": {
        "name": "Precision Time Protocol",
        "category": "Synchronisation",
        "description": "Synchronisation haute précision pour l'industrie.",
        "details": "Précision sous la microseconde. IEEE 1588.",
        "ports": "UDP 319/320",
        "layer": 7,
        "rfc": "IEEE 1588"
    },

    # Voix et vidéo
    "SIP": {
        "name": "Session Initiation Protocol",
        "category": "Voix et vidéo",
        "description": "Établissement, modification et terminaison de sessions multimédia.",
        "details": "Utilisé dans la VoIP. Messages INVITE, BYE, REGISTER...",
        "ports": "UDP/TCP 5060, TLS 5061",
        "layer": 7,
        "rfc": "RFC 3261"
    },
    "RTP": {
        "name": "Real-time Transport Protocol",
        "category": "Voix et vidéo",
        "description": "Transport des médias temps réel (audio/vidéo).",
        "details": "Numéros de séquence et horodatage pour la synchronisation.",
        "ports": "UDP dynamique (pair impair)",
        "layer": 5,
        "rfc": "RFC 3550"
    },
    "RTCP": {
        "name": "RTP Control Protocol",
        "category": "Voix et vidéo",
        "description": "Contrôle qualité et statistiques des sessions RTP.",
        "details": "Rapports sur la perte de paquets et la gigue.",
        "ports": "UDP dynamique (pair impair + 1)",
        "layer": 5,
        "rfc": "RFC 3550"
    },
    "RTSP": {
        "name": "Real Time Streaming Protocol",
        "category": "Voix et vidéo",
        "description": "Contrôle du streaming multimédia.",
        "details": "Commandes PLAY, PAUSE, TEARDOWN. Utilise souvent RTP.",
        "ports": "TCP 554",
        "layer": 7,
        "rfc": "RFC 7826"
    },
    "WebRTC": {
        "name": "Web Real-Time Communication",
        "category": "Voix et vidéo",
        "description": "Communication audio/vidéo et partage de données dans le navigateur.",
        "details": "Utilise SRTP, DTLS, ICE/STUN/TURN.",
        "ports": "UDP dynamique",
        "layer": 7,
        "rfc": "IETF/ W3C"
    },

    # Réseaux sans fil
    "Wi-Fi": {
        "name": "Wireless Fidelity (IEEE 802.11)",
        "category": "Réseaux sans fil",
        "description": "Standards de communication sans fil en bandes ISM.",
        "details": "802.11a/b/g/n/ac/ax/be (Wi-Fi 6/6E/7). Sécurité : WPA2/WPA3.",
        "ports": "N/A",
        "layer": 1,
        "rfc": "IEEE 802.11"
    },
    "Bluetooth": {
        "name": "Bluetooth",
        "category": "Réseaux sans fil",
        "description": "Communication sans fil à courte portée.",
        "details": "2,4 GHz, maître/esclave, protocoles BR/EDR et BLE.",
        "ports": "N/A",
        "layer": 1,
        "rfc": "Bluetooth SIG"
    },
    "Zigbee": {
        "name": "Zigbee",
        "category": "Réseaux sans fil",
        "description": "Réseau maillé basse consommation pour objets connectés.",
        "details": "2,4 GHz, topologies étoile/arbre/maille.",
        "ports": "N/A",
        "layer": 1,
        "rfc": "IEEE 802.15.4"
    },
    "Z-Wave": {
        "name": "Z-Wave",
        "category": "Réseaux sans fil",
        "description": "Protocole sans fil sous-GHz pour domotique.",
        "details": "Bande <1 GHz, maillage, faible consommation.",
        "ports": "N/A",
        "layer": 1,
        "rfc": "Propriétaire (ITU-T G.9959)"
    },
    "LoRaWAN": {
        "name": "Long Range Wide Area Network",
        "category": "Réseaux sans fil",
        "description": "Réseau longue portée basse consommation pour l'IoT.",
        "details": "Topologie étoile, modulation Chirp Spread Spectrum.",
        "ports": "N/A",
        "layer": 1,
        "rfc": "LoRa Alliance"
    },
    "NFC": {
        "name": "Near Field Communication",
        "category": "Réseaux sans fil",
        "description": "Communication sans fil très courte portée.",
        "details": "13,56 MHz. Utilisé pour paiements et badges.",
        "ports": "N/A",
        "layer": 1,
        "rfc": "ISO/IEC 14443, 18092"
    },

    # Internet des objets (IoT)
    "MQTT": {
        "name": "Message Queuing Telemetry Transport",
        "category": "Internet des objets (IoT)",
        "description": "Protocole publish/subscribe léger pour l'IoT.",
        "details": "Broker, topics, QoS 0/1/2. Fonctionne sur TCP.",
        "ports": "TCP 1883, TLS 8883",
        "layer": 7,
        "rfc": "ISO/IEC 20922"
    },
    "CoAP": {
        "name": "Constrained Application Protocol",
        "category": "Internet des objets (IoT)",
        "description": "Protocole web léger pour appareils contraints.",
        "details": "Similaire à HTTP mais sur UDP. Supporte DTLS.",
        "ports": "UDP 5683, DTLS 5684",
        "layer": 7,
        "rfc": "RFC 7252"
    },
    "AMQP": {
        "name": "Advanced Message Queuing Protocol",
        "category": "Internet des objets (IoT)",
        "description": "Protocole de messagerie orienté entreprise.",
        "details": "Files d'attente, échanges, routage. RabbitMQ l'utilise.",
        "ports": "TCP 5672, TLS 5671",
        "layer": 7,
        "rfc": "ISO/IEC 19464"
    },
    "DDS": {
        "name": "Data Distribution Service",
        "category": "Internet des objets (IoT)",
        "description": "Middleware publish/subscribe temps réel.",
        "details": "Utilisé dans l'industrie et les systèmes embarqués.",
        "ports": "Dynamique",
        "layer": 7,
        "rfc": "OMG DDS"
    },
    "XMPP": {
        "name": "Extensible Messaging and Presence Protocol",
        "category": "Internet des objets (IoT)",
        "description": "Messagerie instantanée extensible basée sur XML.",
        "details": "Adresses JID. Historiquement Jabber.",
        "ports": "TCP 5222 (client), 5269 (serveur)",
        "layer": 7,
        "rfc": "RFC 6120"
    },

    # Annuaire
    "LDAP": {
        "name": "Lightweight Directory Access Protocol",
        "category": "Annuaire",
        "description": "Accès et maintenance d'annuaires distribués.",
        "details": "Modèle hiérarchique DIT. Base d'Active Directory.",
        "ports": "TCP/UDP 389",
        "layer": 7,
        "rfc": "RFC 4511"
    },
    "LDAPS": {
        "name": "LDAP Secure",
        "category": "Annuaire",
        "description": "LDAP sur TLS/SSL.",
        "details": "Port 636 historiquement. STARTTLS possible sur 389.",
        "ports": "TCP 636",
        "layer": 7,
        "rfc": "RFC 4513"
    },

    # Virtualisation et VPN
    "OpenVPN": {
        "name": "OpenVPN",
        "category": "Virtualisation et VPN",
        "description": "VPN open-source utilisant TLS/SSL sur UDP ou TCP.",
        "details": "Flexible, supporte TAP et TUN.",
        "ports": "UDP/TCP 1194",
        "layer": 4,
        "rfc": "OpenVPN"
    },
    "WireGuard": {
        "name": "WireGuard",
        "category": "Virtualisation et VPN",
        "description": "VPN moderne, léger et performant.",
        "details": "Cryptographie moderne (Curve25519, ChaCha20, Poly1305).",
        "ports": "UDP dynamique",
        "layer": 3,
        "rfc": "N/A"
    },
    "L2TP": {
        "name": "Layer 2 Tunneling Protocol",
        "category": "Virtualisation et VPN",
        "description": "Tunnel de couche 2, souvent combiné à IPsec.",
        "details": "Ne chiffre pas seul ; IPsec apporte la sécurité.",
        "ports": "UDP 1701",
        "layer": 2,
        "rfc": "RFC 2661"
    },
    "PPTP": {
        "name": "Point-to-Point Tunneling Protocol",
        "category": "Virtualisation et VPN",
        "description": "Ancien protocole VPN, aujourd'hui considéré comme non sûr.",
        "details": "Chiffrement faible (MPPE). Déconseillé.",
        "ports": "TCP 1723, GRE 47",
        "layer": 2,
        "rfc": "RFC 2637"
    },
    "GRE": {
        "name": "Generic Routing Encapsulation",
        "category": "Virtualisation et VPN",
        "description": "Protocole d'encapsulation de paquets dans un tunnel IP.",
        "details": "Utilisé par les VPN site-à-site et PPTP.",
        "ports": "IP 47",
        "layer": 3,
        "rfc": "RFC 2784"
    },

    # Gestion réseau
    "SNMP": {
        "name": "Simple Network Management Protocol",
        "category": "Gestion réseau",
        "description": "Surveillance et gestion des équipements réseau.",
        "details": "MIB, OID, traps, versions v1/v2c/v3.",
        "ports": "UDP 161 (agent), 162 (trap)",
        "layer": 7,
        "rfc": "RFC 3411"
    },
    "NetFlow": {
        "name": "NetFlow",
        "category": "Gestion réseau",
        "description": "Collecte de statistiques de flux par Cisco.",
        "details": "IPFIX est la version standardisée (RFC 7011).",
        "ports": "UDP 2055/9996",
        "layer": 7,
        "rfc": "Propriétaire Cisco / RFC 7011 (IPFIX)"
    },
    "Syslog": {
        "name": "System Logging Protocol",
        "category": "Gestion réseau",
        "description": "Collecte centralisée des journaux système.",
        "details": "Niveaux de sévérité de 0 (Emergency) à 7 (Debug).",
        "ports": "UDP 514, TCP 6514 (TLS)",
        "layer": 7,
        "rfc": "RFC 5424"
    },

    # Industriel
    "Modbus": {
        "name": "Modbus",
        "category": "Industriel",
        "description": "Protocole de communication industriel maître/esclave.",
        "details": "Modbus RTU (série), ASCII, TCP/IP.",
        "ports": "TCP 502",
        "layer": 7,
        "rfc": "Modbus Organization"
    },
    "OPC UA": {
        "name": "OPC Unified Architecture",
        "category": "Industriel",
        "description": "Architecture unifiée pour l'interopérabilité industrielle.",
        "details": "Modèle d'information sécurisé, indépendant des plateformes.",
        "ports": "TCP 4840",
        "layer": 7,
        "rfc": "IEC 62541"
    },
    "CAN Bus": {
        "name": "Controller Area Network",
        "category": "Industriel",
        "description": "Bus de terrain robuste pour systèmes embarqués.",
        "details": "Utilisé dans l'automobile et l'industrie. Trames avec ID.",
        "ports": "N/A",
        "layer": 1,
        "rfc": "ISO 11898"
    },
    "DNP3": {
        "name": "Distributed Network Protocol 3",
        "category": "Industriel",
        "description": "Protocole SCADA pour infrastructures critiques.",
        "details": "Sécurisé via DNP3-SA (Secure Authentication).",
        "ports": "TCP/UDP 20000",
        "layer": 7,
        "rfc": "IEEE 1815"
    },
    "BACnet": {
        "name": "Building Automation and Control Networks",
        "category": "Industriel",
        "description": "Protocole pour la gestion technique des bâtiments.",
        "details": "Objets, propriétés et services normalisés.",
        "ports": "UDP 47808 (BACnet/IP)",
        "layer": 7,
        "rfc": "ANSI/ASHRAE 135"
    },
    "PROFIBUS": {
        "name": "Process Field Bus",
        "category": "Industriel",
        "description": "Standard de bus de terrain pour l'automatisation.",
        "details": "Variantes DP (décentralisée) et PA (processus).",
        "ports": "N/A",
        "layer": 1,
        "rfc": "IEC 61158"
    },
    "EtherCAT": {
        "name": "Ethernet for Control Automation Technology",
        "category": "Industriel",
        "description": "Ethernet temps réel pour l'automatisation industrielle.",
        "details": "Traitement des trames 'on the fly' pour faible latence.",
        "ports": "Ethernet",
        "layer": 1,
        "rfc": "IEC 61158"
    },
}


def get_categories():
    cats = defaultdict(list)
    for acronym, data in PROTOCOLS.items():
        cats[data["category"]].append(acronym)
    return cats


# -----------------------------------------------------------------------------
# Base Frame
# -----------------------------------------------------------------------------

class BaseFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid(row=0, column=0, sticky="nsew")

    def reset(self):
        pass


# -----------------------------------------------------------------------------
# Main Menu
# -----------------------------------------------------------------------------

class MainMenuFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.columnconfigure(0, weight=1)

        title = ttk.Label(
            self,
            text="🌐 Network Protocol Trainer",
            font=("Helvetica", 28, "bold"),
            anchor="center",
        )
        title.grid(row=0, column=0, pady=(40, 20), sticky="ew")

        subtitle = ttk.Label(
            self,
            text="Maîtrisez les acronymes et protocoles réseau",
            font=("Helvetica", 14),
            anchor="center",
        )
        subtitle.grid(row=1, column=0, pady=(0, 30), sticky="ew")

        buttons = [
            ("📚 Mode Apprentissage", lambda: controller.show_frame("LearnFrame")),
            ("❓ Quiz à choix multiples", lambda: controller.show_frame("QuizMCQFrame")),
            ("✏️ Quiz réponse libre", lambda: controller.show_frame("QuizTypeFrame")),
            ("🧩 Quiz association", lambda: controller.show_frame("QuizMatchFrame")),
            ("🔍 Rechercher un protocole", lambda: controller.show_frame("SearchFrame")),
            ("🏆 Statistiques", lambda: controller.show_frame("StatsFrame")),
            ("ℹ️ À propos", self.show_about),
        ]

        for idx, (text, cmd) in enumerate(buttons, start=2):
            btn = ttk.Button(self, text=text, command=cmd, width=35)
            btn.grid(row=idx, column=0, pady=8)

    def show_about(self):
        messagebox.showinfo(
            "À propos",
            "Network Protocol Trainer v1.0\n"
            "Application éducative Tkinter pour apprendre les protocoles réseau.\n"
            "Inclut 80+ protocoles répartis en 16 catégories.",
        )


# -----------------------------------------------------------------------------
# Learning Mode
# -----------------------------------------------------------------------------

class LearnFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        header = ttk.Label(self, text="Mode Apprentissage", font=("Helvetica", 20, "bold"))
        header.grid(row=0, column=0, pady=(20, 10))

        filter_frame = ttk.Frame(self)
        filter_frame.grid(row=1, column=0, pady=10)
        ttk.Label(filter_frame, text="Catégorie :").pack(side="left", padx=5)
        self.category_var = tk.StringVar(value="Toutes")
        self.category_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.category_var,
            state="readonly",
            values=["Toutes"] + sorted(get_categories().keys()),
            width=30,
        )
        self.category_combo.pack(side="left", padx=5)
        self.category_combo.bind("<<ComboboxSelected>>", lambda e: self.populate_list())

        list_frame = ttk.Frame(self)
        list_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            list_frame,
            columns=("acronym", "name", "category", "layer"),
            show="headings",
            selectmode="browse",
        )
        self.tree.heading("acronym", text="Acronyme")
        self.tree.heading("name", text="Nom complet")
        self.tree.heading("category", text="Catégorie")
        self.tree.heading("layer", text="Couche OSI")
        self.tree.column("acronym", width=100, anchor="center")
        self.tree.column("name", width=300)
        self.tree.column("category", width=180)
        self.tree.column("layer", width=100, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        detail_frame = ttk.LabelFrame(self, text="Détails", padding=10)
        detail_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        detail_frame.columnconfigure(0, weight=1)
        self.detail_text = tk.Text(
            detail_frame,
            wrap="word",
            height=10,
            font=("Consolas", 11),
            bg=self.controller.cget("bg"),
            relief="flat",
        )
        self.detail_text.grid(row=0, column=0, sticky="ew")

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=4, column=0, pady=15)
        ttk.Button(btn_frame, text="Retour au menu", command=lambda: controller.show_frame("MainMenuFrame")).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Tout afficher", command=self.populate_list).pack(side="left", padx=5)

    def reset(self):
        self.populate_list()
        self.detail_text.delete("1.0", "end")

    def populate_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        selected_cat = self.category_var.get()
        for acronym, data in sorted(PROTOCOLS.items()):
            if selected_cat == "Toutes" or data["category"] == selected_cat:
                self.tree.insert(
                    "",
                    "end",
                    values=(acronym, data["name"], data["category"], f"{data['layer']:.1f}"),
                )

    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0])
        acronym = item["values"][0]
        data = PROTOCOLS[acronym]
        self.detail_text.delete("1.0", "end")
        self.detail_text.insert("end", f"Acronyme : {acronym}\n")
        self.detail_text.insert("end", f"Nom complet : {data['name']}\n")
        self.detail_text.insert("end", f"Catégorie : {data['category']}\n")
        self.detail_text.insert("end", f"Couche OSI : {data['layer']:.1f}\n")
        self.detail_text.insert("end", f"Ports / Protocole : {data['ports']}\n")
        self.detail_text.insert("end", f"RFC / Standard : {data['rfc']}\n\n")
        self.detail_text.insert("end", f"Description : {data['description']}\n\n")
        self.detail_text.insert("end", f"Détails : {data['details']}\n")


# -----------------------------------------------------------------------------
# Quiz Multiple Choice
# -----------------------------------------------------------------------------

class QuizMCQFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.columnconfigure(0, weight=1)

        self.current_acronym = None
        self.answer = None
        self.streak = 0

        header = ttk.Label(self, text="Quiz à choix multiples", font=("Helvetica", 20, "bold"))
        header.grid(row=0, column=0, pady=(20, 10))

        self.score_label = ttk.Label(self, text="Score : 0", font=("Helvetica", 12))
        self.score_label.grid(row=1, column=0, pady=5)

        self.streak_label = ttk.Label(self, text="Série : 0", font=("Helvetica", 12))
        self.streak_label.grid(row=2, column=0, pady=2)

        self.question_label = ttk.Label(
            self, text="Question", font=("Helvetica", 16, "bold"), wraplength=600, justify="center"
        )
        self.question_label.grid(row=3, column=0, pady=20)

        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.grid(row=4, column=0, pady=10)
        self.choice_buttons = []
        for i in range(4):
            btn = ttk.Button(self.buttons_frame, text=f"Choix {i+1}", width=50, command=lambda i=i: self.check_answer(i))
            btn.grid(row=i, column=0, pady=5)
            self.choice_buttons.append(btn)

        self.feedback_label = ttk.Label(self, text="", font=("Helvetica", 12), foreground="green")
        self.feedback_label.grid(row=5, column=0, pady=10)

        self.hint_label = ttk.Label(self, text="", font=("Helvetica", 10), foreground="blue", wraplength=600)
        self.hint_label.grid(row=6, column=0, pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=7, column=0, pady=15)
        ttk.Button(btn_frame, text="Indice", command=self.show_hint).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Question suivante", command=self.new_question).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Retour au menu", command=lambda: controller.show_frame("MainMenuFrame")).pack(
            side="left", padx=5
        )

    def reset(self):
        self.controller.score = 0
        self.streak = 0
        self.update_score()
        self.new_question()

    def update_score(self):
        self.score_label.config(text=f"Score : {self.controller.score}")
        self.streak_label.config(text=f"Série : {self.streak}")

    def new_question(self):
        self.current_acronym = random.choice(list(PROTOCOLS.keys()))
        correct = PROTOCOLS[self.current_acronym]["name"]
        self.answer = correct

        # Pick 3 distractors from same category if possible
        category = PROTOCOLS[self.current_acronym]["category"]
        same_cat = [a for a, d in PROTOCOLS.items() if d["category"] == category and a != self.current_acronym]
        others = [a for a in PROTOCOLS if a != self.current_acronym and a not in same_cat]
        distractors = []
        if len(same_cat) >= 3:
            distractors = random.sample(same_cat, 3)
        else:
            distractors = same_cat + random.sample(others, 3 - len(same_cat))

        options = [PROTOCOLS[a]["name"] for a in distractors] + [correct]
        random.shuffle(options)
        self.correct_index = options.index(correct)

        self.question_label.config(text=f"Que signifie l'acronyme '{self.current_acronym}' ?")
        for idx, btn in enumerate(self.choice_buttons):
            btn.config(text=options[idx])
        self.feedback_label.config(text="")
        self.hint_label.config(text="")

    def check_answer(self, idx):
        if self.answer is None:
            return
        if idx == self.correct_index:
            self.controller.score += 10 + min(self.streak, 5)
            self.streak += 1
            self.feedback_label.config(foreground="green", text="✅ Correct !")
        else:
            self.streak = 0
            correct_name = self.choice_buttons[self.correct_index].cget("text")
            self.feedback_label.config(
                foreground="red",
                text=f"❌ Faux. La bonne réponse était : {correct_name}",
            )
        self.update_score()

    def show_hint(self):
        if self.current_acronym:
            cat = PROTOCOLS[self.current_acronym]["category"]
            layer = PROTOCOLS[self.current_acronym]["layer"]
            self.hint_label.config(text=f"Indice : catégorie '{cat}', couche OSI {layer:.1f}")


# -----------------------------------------------------------------------------
# Quiz Type-in Answer
# -----------------------------------------------------------------------------

class QuizTypeFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.columnconfigure(0, weight=1)

        self.current_acronym = None
        self.streak = 0

        header = ttk.Label(self, text="Quiz réponse libre", font=("Helvetica", 20, "bold"))
        header.grid(row=0, column=0, pady=(20, 10))

        self.score_label = ttk.Label(self, text="Score : 0", font=("Helvetica", 12))
        self.score_label.grid(row=1, column=0, pady=5)

        self.streak_label = ttk.Label(self, text="Série : 0", font=("Helvetica", 12))
        self.streak_label.grid(row=2, column=0, pady=2)

        self.question_label = ttk.Label(
            self, text="Question", font=("Helvetica", 18, "bold"), wraplength=600, justify="center"
        )
        self.question_label.grid(row=3, column=0, pady=20)

        self.entry = ttk.Entry(self, font=("Helvetica", 14), width=45, justify="center")
        self.entry.grid(row=4, column=0, pady=10)
        self.entry.bind("<Return>", lambda e: self.check_answer())

        self.feedback_label = ttk.Label(self, text="", font=("Helvetica", 12))
        self.feedback_label.grid(row=5, column=0, pady=10)

        self.hint_label = ttk.Label(self, text="", font=("Helvetica", 10), foreground="blue", wraplength=600)
        self.hint_label.grid(row=6, column=0, pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=7, column=0, pady=15)
        ttk.Button(btn_frame, text="Vérifier", command=self.check_answer).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Indice", command=self.show_hint).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Suivant", command=self.new_question).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Retour au menu", command=lambda: controller.show_frame("MainMenuFrame")).pack(
            side="left", padx=5
        )

    def reset(self):
        self.controller.score = 0
        self.streak = 0
        self.update_score()
        self.new_question()

    def update_score(self):
        self.score_label.config(text=f"Score : {self.controller.score}")
        self.streak_label.config(text=f"Série : {self.streak}")

    def new_question(self):
        self.current_acronym = random.choice(list(PROTOCOLS.keys()))
        self.question_label.config(
            text=f"Donnez le nom complet de : {self.current_acronym}"
        )
        self.entry.delete(0, "end")
        self.feedback_label.config(text="")
        self.hint_label.config(text="")
        self.entry.focus_set()

    def normalize(self, text):
        return (
            text.lower()
            .replace("-", " ")
            .replace("_", " ")
            .replace("/", " ")
            .replace("  ", " ")
            .strip()
        )

    def check_answer(self):
        if not self.current_acronym:
            return
        user = self.entry.get()
        correct = PROTOCOLS[self.current_acronym]["name"]
        if self.normalize(user) == self.normalize(correct):
            self.controller.score += 15 + min(self.streak * 2, 10)
            self.streak += 1
            self.feedback_label.config(foreground="green", text=f"✅ Correct ! C'est {correct}")
        else:
            self.streak = 0
            self.feedback_label.config(foreground="red", text=f"❌ Faux. Réponse : {correct}")
        self.update_score()

    def show_hint(self):
        if self.current_acronym:
            correct = PROTOCOLS[self.current_acronym]["name"]
            words = correct.split()
            hint = " ".join([w[:2] + "..." if len(w) > 3 else w for w in words])
            self.hint_label.config(text=f"Indice : {hint}")


# -----------------------------------------------------------------------------
# Quiz Matching
# -----------------------------------------------------------------------------

class QuizMatchFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.columnconfigure(0, weight=1)

        self.items = []
        self.selected_acronym = None
        self.selected_name = None
        self.matched = set()
        self.streak = 0

        header = ttk.Label(self, text="Quiz association", font=("Helvetica", 20, "bold"))
        header.grid(row=0, column=0, pady=(20, 10))

        self.score_label = ttk.Label(self, text="Score : 0", font=("Helvetica", 12))
        self.score_label.grid(row=1, column=0, pady=5)

        self.streak_label = ttk.Label(self, text="Série : 0", font=("Helvetica", 12))
        self.streak_label.grid(row=2, column=0, pady=2)

        self.instruction = ttk.Label(
            self,
            text="Associez chaque acronyme avec son nom complet.",
            font=("Helvetica", 12),
        )
        self.instruction.grid(row=3, column=0, pady=10)

        self.match_frame = ttk.Frame(self)
        self.match_frame.grid(row=4, column=0, pady=10)

        self.acronym_buttons = {}
        self.name_buttons = {}

        self.feedback_label = ttk.Label(self, text="", font=("Helvetica", 12))
        self.feedback_label.grid(row=5, column=0, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=6, column=0, pady=15)
        ttk.Button(btn_frame, text="Nouvelle manche", command=self.new_round).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Retour au menu", command=lambda: controller.show_frame("MainMenuFrame")).pack(
            side="left", padx=5
        )

    def reset(self):
        self.controller.score = 0
        self.streak = 0
        self.update_score()
        self.new_round()

    def update_score(self):
        self.score_label.config(text=f"Score : {self.controller.score}")
        self.streak_label.config(text=f"Série : {self.streak}")

    def clear_frame(self):
        for widget in self.match_frame.winfo_children():
            widget.destroy()
        self.acronym_buttons.clear()
        self.name_buttons.clear()

    def new_round(self):
        self.clear_frame()
        self.selected_acronym = None
        self.selected_name = None
        self.matched = set()
        self.feedback_label.config(text="")

        sample = random.sample(list(PROTOCOLS.keys()), 6)
        self.items = sample

        acronyms = sample[:]
        names = [PROTOCOLS[a]["name"] for a in sample]
        random.shuffle(acronyms)
        random.shuffle(names)

        left_frame = ttk.LabelFrame(self.match_frame, text="Acronymes", padding=10)
        left_frame.pack(side="left", padx=20)
        right_frame = ttk.LabelFrame(self.match_frame, text="Noms complets", padding=10)
        right_frame.pack(side="left", padx=20)

        for a in acronyms:
            btn = tk.Button(
                left_frame,
                text=a,
                width=18,
                font=("Helvetica", 12),
                command=lambda x=a: self.select_acronym(x),
                bg="#e1e1e1",
            )
            btn.pack(pady=3)
            self.acronym_buttons[a] = btn

        for n in names:
            btn = tk.Button(
                right_frame,
                text=n,
                width=40,
                font=("Helvetica", 12),
                command=lambda x=n: self.select_name(x),
                bg="#e1e1e1",
            )
            btn.pack(pady=3)
            self.name_buttons[n] = btn

    def select_acronym(self, acronym):
        if acronym in self.matched:
            return
        self.selected_acronym = acronym
        self.highlight(self.acronym_buttons, acronym, "#aaddff")
        self.try_match()

    def select_name(self, name):
        if name in [PROTOCOLS[a]["name"] for a in self.matched]:
            return
        self.selected_name = name
        self.highlight(self.name_buttons, name, "#aaddff")
        self.try_match()

    def highlight(self, mapping, key, color):
        for k, btn in mapping.items():
            if k in [self.selected_acronym, self.selected_name] or k in self.matched_names():
                continue
            btn.config(bg="#e1e1e1" if k != key else color)

    def matched_names(self):
        return {PROTOCOLS[a]["name"] for a in self.matched}

    def try_match(self):
        if self.selected_acronym is None or self.selected_name is None:
            return
        correct_name = PROTOCOLS[self.selected_acronym]["name"]
        if self.selected_name == correct_name:
            self.controller.score += 10 + min(self.streak, 5)
            self.streak += 1
            self.feedback_label.config(foreground="green", text="✅ Association correcte !")
            self.matched.add(self.selected_acronym)
            self.acronym_buttons[self.selected_acronym].config(bg="#90ee90", state="disabled")
            self.name_buttons[self.selected_name].config(bg="#90ee90", state="disabled")
            if len(self.matched) == len(self.items):
                self.feedback_label.config(
                    foreground="green",
                    text="🎉 Félicitations, vous avez tout associé !",
                )
        else:
            self.streak = 0
            self.feedback_label.config(
                foreground="red",
                text=f"❌ Faux. {self.selected_acronym} n'est pas '{self.selected_name}'.",
            )
            self.acronym_buttons[self.selected_acronym].config(bg="#e1e1e1")
            self.name_buttons[self.selected_name].config(bg="#e1e1e1")
        self.selected_acronym = None
        self.selected_name = None
        self.update_score()


# -----------------------------------------------------------------------------
# Search Frame
# -----------------------------------------------------------------------------

class SearchFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.columnconfigure(0, weight=1)

        header = ttk.Label(self, text="Recherche de protocole", font=("Helvetica", 20, "bold"))
        header.grid(row=0, column=0, pady=(20, 10))

        search_frame = ttk.Frame(self)
        search_frame.grid(row=1, column=0, pady=10)
        ttk.Label(search_frame, text="Rechercher :").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.do_search())
        entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40, font=("Helvetica", 12))
        entry.pack(side="left", padx=5)

        result_frame = ttk.Frame(self)
        result_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        self.result_list = tk.Listbox(result_frame, height=12, font=("Consolas", 12))
        self.result_list.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_list.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_list.config(yscrollcommand=scrollbar.set)
        self.result_list.bind("<<ListboxSelect>>", self.on_select)

        detail_frame = ttk.LabelFrame(self, text="Détails", padding=10)
        detail_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        detail_frame.columnconfigure(0, weight=1)
        self.detail_text = tk.Text(
            detail_frame,
            wrap="word",
            height=12,
            font=("Consolas", 11),
            bg=self.controller.cget("bg"),
            relief="flat",
        )
        self.detail_text.grid(row=0, column=0, sticky="ew")

        ttk.Button(self, text="Retour au menu", command=lambda: controller.show_frame("MainMenuFrame")).grid(
            row=4, column=0, pady=15
        )

    def reset(self):
        self.search_var.set("")
        self.do_search()

    def do_search(self):
        self.result_list.delete(0, "end")
        query = self.search_var.get().lower()
        for acronym, data in sorted(PROTOCOLS.items()):
            text = f"{acronym} {data['name']} {data['category']} {data['description']}"
            if query in text.lower():
                self.result_list.insert("end", f"{acronym} - {data['name']}")

    def on_select(self, event):
        selection = self.result_list.curselection()
        if not selection:
            return
        text = self.result_list.get(selection[0])
        acronym = text.split(" - ")[0]
        data = PROTOCOLS[acronym]
        self.detail_text.delete("1.0", "end")
        self.detail_text.insert("end", f"Acronyme : {acronym}\n")
        self.detail_text.insert("end", f"Nom complet : {data['name']}\n")
        self.detail_text.insert("end", f"Catégorie : {data['category']}\n")
        self.detail_text.insert("end", f"Couche OSI : {data['layer']:.1f}\n")
        self.detail_text.insert("end", f"Ports / Protocole : {data['ports']}\n")
        self.detail_text.insert("end", f"RFC / Standard : {data['rfc']}\n\n")
        self.detail_text.insert("end", f"Description : {data['description']}\n\n")
        self.detail_text.insert("end", f"Détails : {data['details']}\n")


# -----------------------------------------------------------------------------
# Stats Frame
# -----------------------------------------------------------------------------

class StatsFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.columnconfigure(0, weight=1)

        header = ttk.Label(self, text="Statistiques", font=("Helvetica", 20, "bold"))
        header.grid(row=0, column=0, pady=(20, 10))

        self.stats_text = tk.Text(
            self,
            wrap="word",
            height=20,
            font=("Consolas", 12),
            bg=self.controller.cget("bg"),
            relief="flat",
        )
        self.stats_text.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")

        ttk.Button(self, text="Retour au menu", command=lambda: controller.show_frame("MainMenuFrame")).grid(
            row=2, column=0, pady=15
        )

    def reset(self):
        self.stats_text.delete("1.0", "end")
        total = len(PROTOCOLS)
        cats = get_categories()
        lines = [
            f"Nombre total de protocoles : {total}",
            f"Score actuel : {self.controller.score}",
            "",
            "Répartition par catégorie :",
        ]
        for cat in sorted(cats):
            lines.append(f"  • {cat} : {len(cats[cat])} protocole(s)")
        lines.append("")
        lines.append("Répartition par couche OSI :")
        layers = defaultdict(int)
        for data in PROTOCOLS.values():
            layers[int(data["layer"])] += 1
        for layer in sorted(layers):
            lines.append(f"  • Couche {layer} : {layers[layer]} protocole(s)")
        self.stats_text.insert("end", "\n".join(lines))


# -----------------------------------------------------------------------------
# Application Controller
# -----------------------------------------------------------------------------

class NetworkTrainerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network Protocol Trainer")
        self.geometry("900x750")
        self.resizable(True, True)
        self.configure(bg="#f0f0f0")

        self.score = 0

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 11))
        style.configure("TLabel", background="#f0f0f0")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabelframe", background="#f0f0f0")
        style.configure("TLabelframe.Label", background="#f0f0f0", font=("Helvetica", 11, "bold"))

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (
            MainMenuFrame,
            LearnFrame,
            QuizMCQFrame,
            QuizTypeFrame,
            QuizMatchFrame,
            SearchFrame,
            StatsFrame,
        ):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenuFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.reset()
        frame.tkraise()


# -----------------------------------------------------------------------------
# Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    app = NetworkTrainerApp()
    app.mainloop()
