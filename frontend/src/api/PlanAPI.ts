// frontend/src/api/PlanAPI.ts

import Plan from '../types/plan'; // Assuming Plan interface is in types/plan.ts

class PlanAPI {
    private baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    async getPlans(): Promise<Plan[]> {
        const response = await fetch(`${this.baseUrl}/plans`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }

    async getPlan(id: string): Promise<Plan> {
        const response = await fetch(`${this.baseUrl}/plans/${id}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }

    async createPlan(plan: Omit<Plan, 'id'>): Promise<Plan> {
        const response = await fetch(`${this.baseUrl}/plans`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(plan),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }

    async updatePlan(plan: Plan): Promise<Plan> {
        const response = await fetch(`${this.baseUrl}/plans/${plan.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(plan),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }

    async deletePlan(id: string): Promise<void> {
        const response = await fetch(`${this.baseUrl}/plans/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    }
}

export default PlanAPI;
