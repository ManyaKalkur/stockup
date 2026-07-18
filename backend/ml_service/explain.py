import shap

def explain_xgb(model, X):
	explainer= shap.TreeExplainer(model)
	shap_values= explainer.shap_values(X.iloc[[-1]])
	contributions= dict(zip(X.columns, shap_values[0].tolist()))
	ranked= sorted(contributions.items(), key=lambda kv: abs(kv[1]), reverse=True)
	return [{"feature":f,"impact":round(v,4)} for f,v in ranked[:5]]