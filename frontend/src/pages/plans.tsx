// frontend/src/pages/plans.tsx

import React, { useEffect, useState } from 'react';
import PlanAPI from '../api/PlanAPI';
import API_CONFIG from '../config/api';
import Plan from '../types/plan';
import PlanCard from '../components/plan/PlanCard';
import PlanEditor from '../components/plan/PlanEditor';

const PlansPage: React.FC = () => {
    const [plans, setPlans] = useState<Plan[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [showEditor, setShowEditor] = useState<boolean>(false);
    const [editingPlan, setEditingPlan] = useState<Plan | undefined>(undefined); // Plan being edited

    // Initialize PlanAPI with backend URL from config
    const planApi = new PlanAPI(`${API_CONFIG.baseUrl}${API_CONFIG.endpoints.plans}`);

    useEffect(() => {
        fetchPlans();
    }, []);

    const fetchPlans = async () => {
        try {
            setLoading(true);
            const fetchedPlans = await planApi.getPlans();
            setPlans(fetchedPlans);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleCreateNewPlan = () => {
        setEditingPlan(undefined); // Clear any plan being edited
        setShowEditor(true);
    };

    const handleEditPlan = (id: string) => {
        const planToEdit = plans.find(p => p.id === id);
        if (planToEdit) {
            setEditingPlan(planToEdit);
            setShowEditor(true);
        }
    };

    const handleSavePlan = async (plan: Plan) => {
        try {
            await planApi.updatePlan(plan);
            fetchPlans(); // Refresh list
            setShowEditor(false);
        } catch (err: any) {
            setError(err.message);
        }
    };

    const handleCreatePlan = async (plan: Omit<Plan, 'id' | 'created_at' | 'updated_at'>) => {
        try {
            await planApi.createPlan(plan);
            fetchPlans(); // Refresh list
            setShowEditor(false);
        } catch (err: any) {
            setError(err.message);
        }
    };

    const handleDeletePlan = async (id: string) => {
        if (window.confirm('Are you sure you want to delete this plan?')) {
            try {
                await planApi.deletePlan(id);
                fetchPlans(); // Refresh list
            } catch (err: any) {
                setError(err.message);
            }
        }
    };

    const handleViewPlan = (id: string) => {
        // For now, viewing a plan could just log it or navigate to a detail page
        console.log(`Viewing plan with ID: ${id}`);
        // In a real app, this might navigate to /plans/{id}
        // Example: history.push(`/plans/${id}`);
    };

    if (loading) return <div>Loading plans...</div>;
    if (error) return <div className="error-message">Error: {error}</div>;

    return (
        <div className="plans-page">
            <h1>My Plans</h1>
            <button onClick={handleCreateNewPlan} className="create-plan-button">Create New Plan</button>

            <div className="plans-list">
                {plans.length === 0 ? (
                    <p>No plans found. Create one!</p>
                ) : (
                    plans.map(plan => (
                        <PlanCard
                            key={plan.id}
                            plan={plan}
                            onView={handleViewPlan}
                            onEdit={handleEditPlan}
                            onDelete={handleDeletePlan}
                        />
                    ))
                )}
            </div>

            {showEditor && (
                <PlanEditor
                    plan={editingPlan}
                    onSave={handleSavePlan}
                    onCreate={handleCreatePlan}
                    onClose={() => setShowEditor(false)}
                />
            )}
        </div>
    );
};

export default PlansPage;
