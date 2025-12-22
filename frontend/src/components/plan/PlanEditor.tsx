// frontend/src/components/plan/PlanEditor.tsx

import React, { useState } from 'react';
import Plan from '../../types/plan'; // Assuming Plan interface is in types/plan.ts

interface PlanFormProps {
    initialData?: Plan;
    onSubmit: (plan: Omit<Plan, 'id' | 'created_at' | 'updated_at'>) => void; // Omit id for creation
    onCancel: () => void;
}

const PlanForm: React.FC<PlanFormProps> = ({ initialData, onSubmit, onCancel }) => {
    const [name, setName] = useState(initialData?.name || '');
    const [description, setDescription] = useState(initialData?.description || '');
    // Steps editing would be more complex and is simplified here
    const [steps, setSteps] = useState(initialData?.steps || []); 

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // For simplicity, `steps` are not fully editable in this basic form
        onSubmit({ name, description, steps });
    };

    return (
        <form onSubmit={handleSubmit} className="plan-form">
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Plan Name"
                required
            />
            <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Description"
            />
            {/* Future improvement: Add dynamic step editing */}
            <div>
                <h4>Steps (Read-only for now)</h4>
                {steps.length === 0 ? (
                    <p>No steps defined.</p>
                ) : (
                    <ul>
                        {steps.map((step, index) => (
                            <li key={index}>{step.action}</li>
                        ))}
                    </ul>
                )}
            </div>
            <div className="form-actions">
                <button type="submit">Save Plan</button>
                <button type="button" onClick={onCancel}>Cancel</button>
            </div>
        </form>
    );
};


interface PlanEditorProps {
    plan?: Plan; // Optional, for editing existing plan
    onSave: (plan: Plan) => void; // For existing plan update
    onCreate: (plan: Omit<Plan, 'id' | 'created_at' | 'updated_at'>) => void; // For new plan creation
    onClose: () => void;
}

const PlanEditor: React.FC<PlanEditorProps> = ({ plan, onSave, onCreate, onClose }) => {
    const handleSubmit = async (formData: Omit<Plan, 'id' | 'created_at' | 'updated_at'>) => {
        if (plan) {
            // Editing existing plan
            const updatedPlan: Plan = { ...plan, ...formData };
            onSave(updatedPlan);
        } else {
            // Creating new plan
            onCreate(formData);
        }
    };

    return (
        <div className="plan-editor-modal">
            <div className="plan-editor-content">
                <h2>{plan ? `Edit Plan: ${plan.name}` : 'Create New Plan'}</h2>
                <PlanForm initialData={plan} onSubmit={handleSubmit} onCancel={onClose} />
            </div>
        </div>
    );
};

export default PlanEditor;
