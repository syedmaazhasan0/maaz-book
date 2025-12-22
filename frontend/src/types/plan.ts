// frontend/src/types/plan.ts

interface Plan {
    id: string;
    name: string;
    description: string;
    steps: {
        id: string;
        action: string;
        parameters: Record<string, any>;
    }[];
}

export default Plan;
