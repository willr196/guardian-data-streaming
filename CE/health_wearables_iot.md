# Health Wearables IoT System

## Context

You have been assigned to design and develop an [Internet of Things](https://www.ibm.com/topics/internet-of-things) platform focused on health wearables for a local hospice, integrating a heart rate monitoring device alongside a monitoring system capable of overseeing various health-related IoT devices.

## High-level desired outcome

The goal is to create an interconnected ecosystem where health wearables seamlessly communicate with each other and a centralized monitoring system. This system will not only monitor users' heart rate but also facilitate interactions between different health-related devices, triggering actions based on predefined conditions or events.

For instance:

Integrating a heart rate monitor with a smartwatch.

When the heart rate monitor detects abnormal heart rate, it triggers the smartwatch to notify the user. This could also trigger a blood pressure monitor to take additional readings.

These interactions should occur through an [Event Bus](https://aws.amazon.com/event-driven-architecture/), ensuring flexibility and scalability for future integrations.

## Minimum Viable Product

Your project should encompass an IoT platform featuring:

1. A robust Event Bus mechanism enabling communication between connected health wearables and the monitoring system. This includes functionalities for event publishing, subscription, and notification.
2. Implementation of a database to store information regarding connected health wearables, their current statuses, and historical data (e.g., heart rate readings).
3. Integration of at least two health wearables as external components, capable of connecting and disconnecting from the system. One wearable should publish health-related events, while the other should consume them via the Event Bus.

## Non Functional Requirements

- The implementation language is flexible, allowing the use of any programming language deemed suitable for the project.
- The system must prioritize resilience and scalability, ensuring uninterrupted functionality despite failures and accommodating an increasing number of connected health wearables.
- Logging mechanisms should be integrated for comprehensive auditing and debugging purposes, facilitating system maintenance and troubleshooting.
- The code should be well tested.

## Possible Extensions

- Development of an intuitive frontend interface catering to users for device management, health data visualization, and monitoring.
- Implementation of health check mechanisms to assess the operational status of connected health wearables and alerts for unhealthy devices, enhancing overall system reliability.
- Creation of Helm Charts for easy deployment of the service and components to a Kubernetes Cluster if desired.

## Due Date
To be advised, but not later than six weeks from commencement.
