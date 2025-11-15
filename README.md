# Experiment 1: Pendulum vs Rock

## Overview
This experiment implements the first simulation module of the DEC Whitepaper: **Pendulum vs Rock**. It demonstrates the behavior of two distinct agent types responding to a dynamic challenge signal, highlighting the contrast between rigid and adaptive control strategies.

- **Rock**: a rigid, static agent that applies a simple, time-invariant decision function based on instantaneous input.  
- **Pendulum**: an adaptive agent whose response evolves over time, incorporating internal state dynamics (angle and velocity) to modulate decisions.

This experiment is **fully self-contained**; all necessary functions and parameters are included in `main.py`, and no external configuration or utility files are required.

## Purpose
- Illustrate the mechanics of adaptive vs static decision-making within the DEC framework.  
- Provide a reproducible, interactive demonstration of agent dynamics.  
- Serve as an initial module for informal peer review and exploration.  

## Folder Structure
- `main.py` : primary simulation code (`dec_exp01_pendulum_v_rock.py`)  
- `requirements.txt` : Python dependencies (numpy, matplotlib)  
- `README.md` : this file  

> No additional files are necessary; the experiment generates all input data internally and produces interactive plots automatically.

## Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/Calcvlvs-Ethicvs-Dynamicvs-Python.git
cd Calcvlvs-Ethicvs-Dynamicvs-Python/Experiment_1_Pendulum_vs_Rock
pip install -r requirements.txt
