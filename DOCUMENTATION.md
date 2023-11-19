# Documentation

## Table of Contents

- [Documentation](#documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Usage](#usage)
  - [Modules](#modules)
  - [Testing](#testing)
  - [Diagrams](#diagrams)
    - [Packages Diagram](#packages-diagram)
    - [Class Diagram](#class-diagram)

## Introduction

TODO

## Usage

TODO

## Modules

TODO

## Testing

TODO

## Diagrams

### Packages Diagram

  ```plantuml
  @startuml

  package "User Interface Module" {
    [Visualization of Grid]
    [Menus for Selections]
  }

  package "Logic Module" {
    [Sokoban Game Logic]
    [Agent Decision Logic]
  }

  package "AI Module" {
    [Uninformed Search Algorithms]
    [Informed Search Algorithms]
  }

  package "Data Management Module" {
    [Data Reading/Writing]
    [Logging]
  }

  package "Communication Module" {
    [Message Passing]
  }

  "User Interface Module" --> "Logic Module" : Sends user choices\nReceives state updates
  "Logic Module" --> "AI Module" : Receives state & user choices\nSends calculated actions
  "Logic Module" --> "Data Management Module" : Sends state data\nReceives requested data
  "Logic Module" --> "Communication Module" : Exchanges state/action data

  note right of "AI Module" : Involves utilizing\nalgorithms like A*, BFS, etc.

  note right of "Logic Module" : Core of the application,\ninteracting with all modules.

  @enduml
  ```

  ![Packages Diagram](./packages_diagram.png)

### Class Diagram

TODO

  ```plantuml
  @startuml

  class "mesa.Agent" as Agent {
      +step()
  }

  class "mesa.Model" as Model {
      +step()
  }

  interface "IMovable" {
      +move()
  }

  interface "IPushable" {
      +push()
  }

  class "Wall" as Wall implements DrawableAgent {

  }

  interface "IAlgorithm" {
      +calculateMove()
  }

  class "Box" as Box implements IPushable, DrawableAgent {

  }

  class "Robot" as Robot implements IMovable, DrawableAgent {
      -algorithm: IAlgorithm
      +step()
      +setAlgorithm(algorithm: IAlgorithm)
  }

  class "Target" as Target implements DrawableAgent {

  }

  class "Floor" as Floor implements DrawableAgent {

  }

  class "BFS" implements IAlgorithm {

  }

  class "DFS" implements IAlgorithm {

  }

  class "UCS" implements IAlgorithm {

  }

  class "BeamSearch" implements IAlgorithm {

  }

  class "HillClimbing" implements IAlgorithm {

  }

  class "AStar" implements IAlgorithm {

  }

  class "SokobanModel" as SModel {
      +step()
      +addAgent(agent: mesa.Agent)
  }

  interface "DrawableAgent" {
      +getImage()
      +getLayer()
  }

  Agent <|-- Wall
  Agent <|-- Box
  Agent <|-- Robot
  Agent <|-- Target
  Agent <|-- Floor

  Model <|-- SModel

  Robot ..> IAlgorithm : uses
  Robot ..> IPushable : pushes

  SModel "1" -- "0..*" Agent : contains

  @enduml
  ```
