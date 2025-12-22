// frontend/src/components/plan/PlanCard.tsx

import React from 'react';
import Plan from '../../types/plan'; // Assuming Plan interface is in types/plan.ts

interface PlanCardProps {
    plan: Plan;
    onView: (id: string) => void;
    onEdit: (id: string) => void;
    onDelete: (id: string) => void;
}

const PlanCard: React.FC<PlanCardProps> = ({ plan, onView, onEdit, onDelete }) => {
    return (
        <div className="card">
            <h3>{plan.name}</h3>
            <p>{plan.description}</p>
            <div className="actions">
                <button onClick={() => onView(plan.id)}>View</button>
                <button onClick={() => onEdit(plan.id)}>Edit</button>
                <button onClick={() => onDelete(plan.id)}>Delete</button>
            </div>
        </div>
    );
};

export default PlanCard;
